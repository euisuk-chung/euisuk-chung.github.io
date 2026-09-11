"""OKF(Open Knowledge Format) 공용 유틸리티.

크롤러(blog_crawler.py), 마이그레이션(okf_migrate.py), 린트(okf_lint.py),
인덱스(okf_index.py)가 함께 쓰는 순수 함수 모음. 외부 의존성은 PyYAML뿐이다.

포맷 규칙은 _doc/Manual.md 의 "OKF 콘텐츠 규칙" 절을 따른다.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# --- 경로 상수 -------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

# 포스트 front matter 키 순서. 여기 없는 키는 정렬해서 뒤에 붙인다.
POST_KEY_ORDER = [
    "type", "title", "description", "date", "tags", "resource",
    "generated", "sources", "status", "year",
]
# 태그 concept front matter 키 순서.
CONCEPT_KEY_ORDER = [
    "type", "title", "slug", "description", "aliases", "parent", "related",
    "generated", "status",
]
STATUS_VALUES = ("draft", "stable", "deprecated")
# OKF §7 actor: <producer>/<version> | human:<id> | process:<id>
ACTOR_RE = re.compile(r"^(human:[\w.-]+|process:[\w.-]+|[\w.-]+/[\w.-]+)$")
ISO_DT_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2}))?$"
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
POST_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BOM = "﻿"

# --- 본문 구문 정규식 -----------------------------------------------------
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
RAW_OPEN = "{% raw %}"
RAW_CLOSE = "{% endraw %}"
# setext 밑줄: 같은 문자 2개 이상 (kramdown 은 1개도 허용하지만 markdownify 는 항상 길게 쓴다)
UNDERLINE_RE = re.compile(r"^ {0,3}(?P<c>-|=)(?P=c)+[ \t]*$")
ATX_RE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
ATX_STRIP_RE = re.compile(r"^ {0,3}#{1,6}[ \t]+")
HR_RE = re.compile(r"^ {0,3}-{3,}[ \t]*$")
TABLE_ROW_RE = re.compile(r"^ {0,3}\|")
BLOCKQUOTE_RE = re.compile(r"^ {0,3}>")
INDENTED_CODE_RE = re.compile(r"^(?: {4}|\t)")
TITLE_PREFIX_RE = re.compile(r"^\[([^\]]+)\]")


# --- 설정 -------------------------------------------------------------------
def load_config() -> dict:
    """_scripts/config.json 을 읽는다. posts_dir / concepts_dir / okf_root 기본값 포함."""
    cfg_path = SCRIPT_DIR / "config.json"
    cfg = {}
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg.setdefault("posts_dir", "okf/_posts")
    cfg.setdefault("concepts_dir", "okf/_concepts")
    cfg.setdefault("okf_root", "okf")
    return cfg


def load_types_config() -> dict:
    p = SCRIPT_DIR / "okf_types.json"
    return json.loads(p.read_text(encoding="utf-8"))


# --- YAML 입출력 ------------------------------------------------------------
def yaml_dq(value) -> str:
    """YAML 이중따옴표 스칼라. 백슬래시와 따옴표를 이스케이프한다.

    제목에 따옴표가 든 글을 그대로 쓰면 front matter 가 깨져 Jekyll 이
    해당 포스트를 레이아웃 없이 렌더한다.
    """
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


@dataclass
class ParsedDoc:
    front_matter: dict
    body: str
    had_bom: bool = False
    fm_text: str = ""
    has_front_matter: bool = True


def parse_document(text: str) -> ParsedDoc:
    """마크다운 문서를 (front matter, body) 로 나눈다. BOM 은 제거한다."""
    had_bom = text.startswith(BOM)
    if had_bom:
        text = text[len(BOM):]
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return ParsedDoc({}, text, had_bom, "", has_front_matter=False)
    end = text.find("\n---", 4)
    while end != -1:
        # 닫는 --- 는 줄 전체가 --- 여야 한다
        line_end = text.find("\n", end + 1)
        closing = text[end + 1:line_end if line_end != -1 else None]
        if closing.rstrip() == "---":
            break
        end = text.find("\n---", end + 1)
    if end == -1:
        return ParsedDoc({}, text, had_bom, "", has_front_matter=False)
    fm_text = text[4:end + 1]
    rest_start = text.find("\n", end + 1)
    body = "" if rest_start == -1 else text[rest_start + 1:]
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        raise ValueError("front matter is not a mapping")
    return ParsedDoc(data, body, had_bom, fm_text)


def _emit_value(key: str, value, indent: int, out: list[str]) -> None:
    pad = " " * indent
    if isinstance(value, dict):
        out.append(f"{pad}{key}:")
        for k, v in value.items():
            _emit_value(k, v, indent + 2, out)
    elif isinstance(value, list):
        if not value:
            out.append(f"{pad}{key}: []")
            return
        out.append(f"{pad}{key}:")
        for item in value:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    sub: list[str] = []
                    _emit_value(k, v, indent + 4, sub)
                    if first:
                        sub[0] = f"{pad}  - " + sub[0].lstrip()
                        first = False
                    out.extend(sub)
            else:
                out.append(f"{pad}  - {_scalar(item)}")
    else:
        out.append(f"{pad}{key}: {_scalar(value)}")


def _scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return yaml_dq(value)


def render_front_matter(data: dict, key_order: list[str] = POST_KEY_ORDER) -> str:
    """결정적 front matter 문자열('---' 포함, 끝에 개행)."""
    out: list[str] = ["---"]
    ordered = [k for k in key_order if k in data and data[k] is not None]
    extras = sorted(k for k in data if k not in key_order and data[k] is not None)
    for k in ordered + extras:
        _emit_value(k, data[k], 0, out)
    out.append("---")
    return "\n".join(out) + "\n"


# --- 본문 처리 --------------------------------------------------------------
def code_mask(lines: list[str]) -> list[bool]:
    """각 줄이 코드(펜스/raw) 영역 안인지 표시한다. 펜스 줄 자체도 True."""
    mask = [False] * len(lines)
    fence_char = None
    fence_len = 0
    in_raw = False
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if fence_char is None and not in_raw:
            if stripped == RAW_OPEN:
                in_raw = True
                mask[i] = True
                continue
            m = FENCE_RE.match(ln)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                mask[i] = True
                continue
            mask[i] = False
        elif in_raw:
            mask[i] = True
            if stripped == RAW_CLOSE:
                in_raw = False
        else:
            mask[i] = True
            m = FENCE_RE.match(ln)
            if m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len \
                    and ln.strip(" \t") == m.group(1):
                fence_char = None
    return mask


def _unescape_md(text: str) -> str:
    return re.sub(r"\\([\\`*_{}\[\]()#+\-.!|<>~\"'])", r"\1", text)


def _norm_title(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", _unescape_md(text)).split())


@dataclass
class BodyReport:
    h1_removed: bool = False
    h1_kept: bool = False
    bom_stripped: bool = False
    setext_converted: int = 0
    list_marker_headings: list[int] = field(default_factory=list)
    hr_removed: int = 0
    ambiguous: list[int] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "h1_removed": self.h1_removed,
            "h1_kept": self.h1_kept,
            "bom_stripped": self.bom_stripped,
            "setext_converted": self.setext_converted,
            "list_marker_headings": self.list_marker_headings,
            "hr_removed": self.hr_removed,
            "ambiguous": self.ambiguous,
        }


def remove_duplicate_h1(lines: list[str], title: str, report: BodyReport) -> list[str]:
    """본문 선두의 `# {title}` (여러 줄로 접힌 경우 포함) 을 제거한다."""
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or not lines[i].startswith("# "):
        return lines
    j = i
    run: list[str] = []
    while j < len(lines) and lines[j].strip():
        run.append(lines[j].strip())
        j += 1
    joined = " ".join(run)[2:]  # "# " 제거
    folded_title = _norm_title(" ".join(title.split()))
    if _norm_title(joined) != folded_title:
        report.h1_kept = True
        return lines
    while j < len(lines) and not lines[j].strip():
        j += 1
    report.h1_removed = True
    return lines[:i] + lines[j:]


def setext_to_atx(lines: list[str], report: BodyReport) -> list[str]:
    """setext 헤딩(text + ===/---) 을 ATX(# / ##) 로 바꾼다. 코드 영역은 건드리지 않는다."""
    mask = code_mask(lines)
    out = list(lines)
    drop: set[int] = set()
    for i in range(1, len(lines)):
        if mask[i] or mask[i - 1]:
            continue
        m = UNDERLINE_RE.match(lines[i])
        if not m:
            continue
        prev = lines[i - 1]
        if not prev.strip():
            continue  # 빈 줄 뒤 --- 는 hr
        if INDENTED_CODE_RE.match(prev) or ATX_RE.match(prev) or FENCE_RE.match(prev) \
                or TABLE_ROW_RE.match(prev) or BLOCKQUOTE_RE.match(prev) \
                or UNDERLINE_RE.match(prev) or HR_RE.match(prev):
            continue
        if i >= 2 and lines[i - 2].strip() and not mask[i - 2] \
                and not ATX_RE.match(lines[i - 2]) and not UNDERLINE_RE.match(lines[i - 2]) \
                and not HR_RE.match(lines[i - 2]):
            # 두 줄 이상 문단 뒤 밑줄: 문단 전체가 헤딩이 된다. 손대지 않고 보고만 한다.
            report.ambiguous.append(i + 1)
            continue
        text = prev.strip()
        if text.endswith("#") and not text.endswith("\\#"):
            text = text[:-1] + "\\#"
        level = "#" if m.group("c") == "=" else "##"
        out[i - 1] = f"{level} {text}"
        drop.add(i)
        report.setext_converted += 1
        if re.match(r"^\s*(\d+\.|[*+-])\s", prev):
            report.list_marker_headings.append(i)
    return [ln for k, ln in enumerate(out) if k not in drop]


def remove_hr_before_heading(lines: list[str], report: BodyReport) -> list[str]:
    """빈 줄 뒤 `---` 규칙의 다음 비공백 줄이 ATX 헤딩이면 규칙(과 사이 빈 줄)을 지운다."""
    mask = code_mask(lines)
    drop: set[int] = set()
    for i, ln in enumerate(lines):
        if mask[i] or not HR_RE.match(ln):
            continue
        if i > 0 and lines[i - 1].strip():
            continue  # 앞 줄이 비어있지 않으면 setext 밑줄이므로 건너뜀
        if i in drop:
            continue
        # 연속된 `---` (빈 줄로 구분) 는 하나의 규칙 묶음으로 본다
        j = i + 1
        hr_count = 1
        while j < len(lines) and (not lines[j].strip() or (not mask[j] and HR_RE.match(lines[j]))):
            if lines[j].strip():
                hr_count += 1
            j += 1
        if j < len(lines) and not mask[j] and ATX_RE.match(lines[j]):
            for k in range(i, j):
                drop.add(k)
            report.hr_removed += hr_count
    return [ln for k, ln in enumerate(lines) if k not in drop]


def normalize_body(body: str, title: str | None = None) -> tuple[str, BodyReport]:
    """본문 정규화: 중복 H1 제거 → setext→ATX → 제목 앞 hr 제거. 그 외는 바이트 동일."""
    report = BodyReport()
    trailing_newline = body.endswith("\n")
    lines = body.split("\n")
    if trailing_newline:
        lines = lines[:-1]
    if title:
        lines = remove_duplicate_h1(lines, title, report)
    lines = setext_to_atx(lines, report)
    lines = remove_hr_before_heading(lines, report)
    text = "\n".join(lines)
    if trailing_newline or not text.endswith("\n"):
        text += "\n"
    return text, report


def _canonical_lines(lines: list[str]) -> tuple[list[str], int, int]:
    """(내용 줄 목록, setext 밑줄 수, ATX 헤딩 수). 빈 줄·밑줄·hr 은 버리고 ATX 마커는 벗긴다."""
    mask = code_mask(lines)
    out: list[str] = []
    setext = atx = 0
    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        if not mask[i] and (UNDERLINE_RE.match(ln) or HR_RE.match(ln)):
            if i > 0 and lines[i - 1].strip() and not mask[i - 1] and UNDERLINE_RE.match(ln) \
                    and not ATX_RE.match(lines[i - 1]) and not UNDERLINE_RE.match(lines[i - 1]) \
                    and not HR_RE.match(lines[i - 1]):
                setext += 1
            continue
        t = ln
        if not mask[i] and ATX_RE.match(ln):
            atx += 1
            t = ATX_STRIP_RE.sub("", ln)
        t = t.strip()
        if t.endswith("\\#"):
            t = t[:-2] + "#"
        out.append(t)
    return out, setext, atx


def verify_no_loss(before: str, after: str, title: str | None = None) -> list[str]:
    """정규화가 허용된 변경만 했는지 검사한다. 위반 목록(문자열)을 돌려준다.

    허용되는 차이: 선두 중복 H1 제거, 빈 줄/setext 밑줄/hr 줄 삭제, `text` → `## text`.
    내용 줄 시퀀스(마커·밑줄·hr·빈 줄 제외)가 같아야 하고, 사라진 setext 밑줄 수만큼 ATX 헤딩이 늘어야 한다.
    """
    import difflib

    b = before.lstrip(BOM).replace("\r\n", "\n").split("\n")
    if title:
        b = remove_duplicate_h1(b, title, BodyReport())
    a = after.split("\n")
    cb, setext_b, atx_b = _canonical_lines(b)
    ca, setext_a, atx_a = _canonical_lines(a)
    problems: list[str] = []
    if cb != ca:
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, cb, ca, autojunk=False).get_opcodes():
            if tag == "equal":
                continue
            problems.append(f"content differs near line {i1 + 1}: {cb[i1:i2][:2]!r} -> {ca[j1:j2][:2]!r}")
    if (setext_b - setext_a) != (atx_a - atx_b):
        problems.append(f"heading count mismatch: setext {setext_b}->{setext_a}, atx {atx_b}->{atx_a}")
    return problems


# --- 태그 어휘 -------------------------------------------------------------
@dataclass
class Concept:
    path: Path
    title: str
    slug: str
    description: str = ""
    aliases: list[str] = field(default_factory=list)
    parent: str | None = None
    related: list[str] = field(default_factory=list)
    status: str = "stable"
    data: dict = field(default_factory=dict)


def load_concepts(concepts_dir: Path) -> dict[str, Concept]:
    """concepts_dir/*.md 를 읽어 title -> Concept 로 돌려준다."""
    result: dict[str, Concept] = {}
    if not concepts_dir.exists():
        return result
    for p in sorted(concepts_dir.glob("*.md")):
        doc = parse_document(p.read_text(encoding="utf-8"))
        fm = doc.front_matter
        if not fm.get("title"):
            continue
        c = Concept(
            path=p,
            title=str(fm["title"]),
            slug=str(fm.get("slug") or p.stem),
            description=str(fm.get("description") or ""),
            aliases=[str(a) for a in (fm.get("aliases") or [])],
            parent=fm.get("parent"),
            related=[str(r) for r in (fm.get("related") or [])],
            status=str(fm.get("status") or "stable"),
            data=fm,
        )
        result[c.title] = c
    return result


def build_alias_map(concepts: dict[str, Concept]) -> dict[str, str]:
    """alias(및 title 의 소문자형) -> canonical title."""
    amap: dict[str, str] = {}
    for c in concepts.values():
        amap[c.title] = c.title
        amap[c.title.casefold()] = c.title
        for a in c.aliases:
            amap[a] = c.title
            amap[a.casefold()] = c.title
    return amap


def canonicalize_tags(tags: list[str], alias_map: dict[str, str]) -> tuple[list[str], list[str]]:
    """태그를 정규 title 로 바꾼다. (정규화된 목록, 어휘에 없는 태그 목록)."""
    out: list[str] = []
    unknown: list[str] = []
    for t in tags:
        t = str(t).strip()
        if not t:
            continue
        canon = alias_map.get(t) or alias_map.get(t.casefold())
        if canon is None:
            unknown.append(t)
            canon = t
        if canon not in out:
            out.append(canon)
    return out, unknown


# --- type 유도 --------------------------------------------------------------
def derive_type(title: str, types_cfg: dict, fallback: str | None = None) -> str:
    m = TITLE_PREFIX_RE.match(title or "")
    if m:
        key = m.group(1).strip()
        pm = types_cfg.get("prefix_map", {})
        if key in pm:
            return pm[key]
    for pattern, t in types_cfg.get("regex_map", {}).items():
        if re.search(pattern, title or ""):
            return t
    return fallback or types_cfg.get("default", "Blog Post")


# --- 포스트 열거 ------------------------------------------------------------
def iter_post_files(posts_dir: Path) -> list[Path]:
    """날짜 파일명 규칙에 맞는 포스트만 (Jekyll 이 포스트로 인식하는 파일)."""
    files = []
    for p in sorted(posts_dir.rglob("*.md")):
        if any(part.startswith("_") for part in p.relative_to(posts_dir).parts[:-1]):
            continue  # _draft, _archived
        if POST_FILENAME_RE.match(p.name):
            files.append(p)
    return files


def resolve_path(p: str) -> Path:
    """CLI 경로 인자: 절대 경로 → 그대로, 상대 경로 → cwd 기준, 없으면 레포 루트 기준."""
    pp = Path(p)
    if pp.is_absolute():
        return pp
    if pp.exists():
        return pp.resolve()
    return REPO_ROOT / pp


def rel_posix(p: Path, root: Path = REPO_ROOT) -> str:
    return unicodedata.normalize("NFC", p.resolve().relative_to(root.resolve()).as_posix())
