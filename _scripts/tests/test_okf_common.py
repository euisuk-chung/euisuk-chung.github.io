import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import okf_common as oc  # noqa: E402


def norm(body, title="T"):
    out, rep = oc.normalize_body(body, title)
    assert not oc.verify_no_loss(body, out, title), oc.verify_no_loss(body, out, title)
    return out, rep


def test_setext_h2_and_h1():
    body = "Intro\n-----\n\ntext\n\nBig\n===\n\nmore\n"
    out, rep = norm(body)
    assert out == "## Intro\n\ntext\n\n# Big\n\nmore\n"
    assert rep.setext_converted == 2


def test_numbered_setext_becomes_real_heading():
    body = "1. Introduction\n---------------\n\np\n"
    out, rep = norm(body)
    assert out == "## 1. Introduction\n\np\n"
    assert rep.list_marker_headings == [1]  # 1-based line of the heading text


def test_bullet_setext():
    out, _ = norm("* item\n---\n\np\n")
    assert out == "## * item\n\np\n"


def test_hr_after_blank_is_kept_unless_before_heading():
    body = "para\n\n---\n\npara2\n\n---\n\nHead\n----\n\nx\n"
    out, rep = norm(body)
    assert out == "para\n\n---\n\npara2\n\n## Head\n\nx\n"
    assert rep.hr_removed == 1


def test_hr_directly_before_atx():
    out, rep = norm("a\n\n---\n## B\nc\n")
    assert out == "a\n\n## B\nc\n"
    assert rep.hr_removed == 1


def test_fenced_code_untouched():
    body = "```yaml\nkey: v\n---\nfoo\n---\n```\n\nHead\n---\n"
    out, rep = norm(body)
    assert out == "```yaml\nkey: v\n---\nfoo\n---\n```\n\n## Head\n"
    assert rep.setext_converted == 1


def test_raw_block_untouched():
    body = "{% raw %}\n```\n{{x}}\n---\n```\n{% endraw %}\n\nH\n===\n"
    out, _ = norm(body)
    assert out.startswith("{% raw %}\n```\n{{x}}\n---\n```\n{% endraw %}\n\n# H\n")


def test_duplicate_h1_removed_only_when_matching_title():
    out, rep = norm("# Hello World\n\nbody\n", title="Hello World")
    assert out == "body\n" and rep.h1_removed
    out, rep = norm("# Other\n\nbody\n", title="Hello World")
    assert out == "# Other\n\nbody\n" and rep.h1_kept


def test_multiline_h1_matches_folded_title():
    out, rep = norm("# Part one\nPart two\n\nbody\n", title="Part one Part two")
    assert out == "body\n" and rep.h1_removed


def test_escaped_h1_matches_title():
    out, rep = norm("# A \\*B\\* C\n\nbody\n", title="A *B* C")
    assert rep.h1_removed


def test_bom_stripped_and_front_matter_parsed():
    doc = oc.parse_document("﻿---\ntitle: \"x\"\n---\n\nbody\n")
    assert doc.had_bom and doc.front_matter == {"title": "x"} and doc.body == "\nbody\n"


def test_trailing_hash_escaped():
    out, _ = norm("C#\n---\n")
    assert out == "## C\\#\n"


def test_ambiguous_multiline_paragraph_left_alone():
    body = "line one\nline two\n---\n"
    out, rep = norm(body)
    assert out == body and rep.ambiguous == [3]


def test_blockquote_and_table_not_converted():
    body = "> quote\n---\n\n| a | b |\n---\n"
    out, rep = norm(body)
    assert out == body and rep.setext_converted == 0


def test_idempotent():
    body = "# T\n\nA\n---\n\n---\n\nB\n===\n"
    once, _ = norm(body)
    twice, rep = oc.normalize_body(once, "T")
    assert once == twice and rep.setext_converted == 0 and rep.hr_removed == 0


def test_verify_no_loss_catches_deleted_paragraph():
    assert oc.verify_no_loss("a\n\nb\n", "a\n")


def test_render_front_matter_order_and_quoting():
    fm = {"year": "2024", "title": 'He said "hi"', "type": "Tip", "tags": ["A", "B"],
          "generated": {"by": "process:velog-sync", "at": "2024-01-01T00:00:00Z"}, "zzz": True}
    text = oc.render_front_matter(fm)
    assert text == ('---\ntype: "Tip"\ntitle: "He said \\"hi\\""\ntags:\n  - "A"\n  - "B"\n'
                    'generated:\n  by: "process:velog-sync"\n  at: "2024-01-01T00:00:00Z"\n'
                    'year: "2024"\nzzz: true\n---\n')
    assert oc.parse_document(text).front_matter == fm


def test_render_sources_list_of_maps():
    fm = {"type": "Tip", "sources": [{"id": "velog", "resource": "https://x"}]}
    text = oc.render_front_matter(fm)
    assert 'sources:\n  - id: "velog"\n    resource: "https://x"\n' in text
    assert oc.parse_document(text).front_matter == fm


def test_canonicalize_tags_with_aliases():
    concepts = {"ChatGPT": oc.Concept(Path("x"), "ChatGPT", "chatgpt", aliases=["chatGPT"])}
    amap = oc.build_alias_map(concepts)
    tags, unknown = oc.canonicalize_tags(["chatGPT", "chatgpt", "Foo"], amap)
    assert tags == ["ChatGPT", "Foo"] and unknown == ["Foo"]


def test_derive_type():
    cfg = {"default": "Blog Post", "prefix_map": {"Paper Review": "Paper Review"},
           "regex_map": {"^\\[Day \\d+\\]": "Product Update"}}
    assert oc.derive_type("[Paper Review] X", cfg) == "Paper Review"
    assert oc.derive_type("[Day 3] X", cfg) == "Product Update"
    assert oc.derive_type("plain", cfg) == "Blog Post"


def test_migrate_text_is_idempotent(tmp_path):
    import okf_migrate as om
    ctx = {"rows": [], "overrides": {}, "types_cfg": oc.load_types_config(), "alias_map": {}}
    src = '---\ntitle: "T"\ndate: "2021-01-01"\nyear: "2021"\n---\n\n# T\n\nA\n---\n\nbody\n'
    once, _ = om.migrate_text(src, "okf/_posts/2021/2021-01-01-T.md", ctx, {"description": "설명."})
    twice, _ = om.migrate_text(once, "okf/_posts/2021/2021-01-01-T.md", ctx, None)
    assert once == twice
    assert once.endswith('---\n\n## A\n\nbody\n')
