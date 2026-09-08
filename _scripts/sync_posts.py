import argparse
import logging
import os
import re
import shutil
import unicodedata

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def _normalize_for_dedup(filename):
    """
    파일명을 정규화하여 중복 비교에 사용합니다.
    크롤러의 sanitize 규칙(&→and, '→_ 등)과 원본 파일명의 차이를 흡수합니다.

    Returns: (date_str, normalized_title)
    """
    name = filename.replace('.md', '')

    # 날짜(YYYY-MM-DD)와 제목 분리
    date_part = name[:10]
    title_part = name[11:] if len(name) > 11 else ''

    # & ↔ and 통일
    title_part = title_part.replace('&', 'and')

    # 다양한 따옴표 문자 제거
    for ch in ["'", "\u2018", "\u2019", '"', '\u201c', '\u201d']:
        title_part = title_part.replace(ch, '')

    # _ 와 공백 통일, 하이픈도 공백으로
    title_part = title_part.replace('_', ' ').replace('-', ' ')

    # 이모지/특수 유니코드 기호 제거
    title_part = ''.join(
        c for c in title_part
        if not unicodedata.category(c).startswith(('So', 'Sk', 'Sc'))
    )

    # 연속 공백 정리
    title_part = re.sub(r'\s+', ' ', title_part).strip().lower()

    return date_part, title_part


def remove_duplicate_posts(source_dir, target_posts_dir, dry_run=False):
    """
    sync 후 target에 남아 있는 구버전 파일(특수문자 포함 파일명)을 찾아 제거합니다.

    크롤러가 파일명을 sanitize(&→and, '→_ 등)하면서 동일 글이
    다른 이름으로 두 벌 존재하게 되는 문제를 해결합니다.
    """
    # 크롤러(source) 파일명 수집 - 이것이 정본(canonical)
    source_files = {}  # (date, norm_title) -> rel_path
    source_rel_set = set()
    for root, _dirs, files in os.walk(source_dir):
        for f in files:
            if f.endswith('.md'):
                rel = os.path.relpath(os.path.join(root, f), source_dir)
                source_rel_set.add(rel)
                date_part, norm_title = _normalize_for_dedup(f)
                source_files[(date_part, norm_title)] = rel

    # 블로그(target) 파일 중 source에 없는 것만 검사
    removed = 0
    for root, _dirs, files in os.walk(target_posts_dir):
        for f in files:
            if not f.endswith('.md'):
                continue

            rel = os.path.relpath(os.path.join(root, f), target_posts_dir)
            if rel in source_rel_set:
                continue  # 크롤러 정본과 동일 파일명 → 유지

            # 이 파일이 크롤러 정본의 "구버전 이름"인지 확인
            date_part, norm_title = _normalize_for_dedup(f)
            key = (date_part, norm_title)

            matched_source = None
            if key in source_files:
                matched_source = source_files[key]
            else:
                # fuzzy: 같은 날짜 + 제목 앞 30자 일치
                for (sd, st), srel in source_files.items():
                    if sd == date_part and len(norm_title) > 10 and (
                        st.startswith(norm_title[:30]) or norm_title.startswith(st[:30])
                    ):
                        matched_source = srel
                        break

            if matched_source and matched_source != rel:
                full_path = os.path.join(root, f)
                if dry_run:
                    logging.info(f"[Dry Run] Would delete duplicate: {rel} (kept: {matched_source})")
                else:
                    os.remove(full_path)
                    logging.info(f"[Dedup] Deleted: {rel} (kept: {matched_source})")
                    removed += 1

    if removed > 0:
        logging.info(f"[Dedup] Removed {removed} duplicate post(s).")
    else:
        logging.info("[Dedup] No duplicates found.")

    return removed


def sync_posts(
    source_dir=None,
    target_repo_dir=None,
    post_folder_name="_posts",
    dry_run=False
):
    """
    블로그 포스팅 마크다운 파일들을 euisuk-chung.github.io 레포로 복사합니다.

    Parameters
    ----------
    source_dir : str
        Velog 백업 디렉토리 경로.
    target_repo_dir : str
        GitHub Pages 레포지토리 경로.
    post_folder_name : str
        GitHub 블로그 레포 내 실제 포스팅 폴더 이름.
    dry_run : bool
        True이면 파일 복사 없이 작업 계획만 출력.
    """

    # Default paths
    if source_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.join(current_dir, "_posts")

    if target_repo_dir is None:
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_repo_dir = os.path.join(parent_dir, "euisuk-chung.github.io")

    target_posts_dir = os.path.join(target_repo_dir, post_folder_name)

    logging.info(f"Source Directory: {source_dir}")
    logging.info(f"Target Repository: {target_repo_dir}")
    logging.info(f"Target Posts Directory: {target_posts_dir}")
    logging.info(f"Dry Run Mode: {'Enabled' if dry_run else 'Disabled'}")

    # Validate source directory
    if not os.path.exists(source_dir):
        logging.error(f"Source directory '{source_dir}' does not exist.")
        return

    years = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

    if not years:
        logging.info(f"No year-based folders found in '{source_dir}'.")
        return

    # --- Step 1: 파일 복사 ---
    for year_folder in years:
        year_path = os.path.join(source_dir, year_folder)
        target_year_path = os.path.join(target_posts_dir, year_folder)

        # Ensure target year directory exists
        try:
            if not os.path.exists(target_year_path):
                if dry_run:
                    logging.info(f"[Dry Run] Would create directory: {target_year_path}")
                else:
                    os.makedirs(target_year_path, exist_ok=True)
                    logging.info(f"Created directory: {target_year_path}")
        except Exception as e:
            logging.error(f"Failed to create directory '{target_year_path}': {e}")
            continue

        # Process markdown files
        for file_name in os.listdir(year_path):
            if file_name.endswith(".md"):
                source_file_path = os.path.join(year_path, file_name)
                target_file_path = os.path.join(target_year_path, file_name)

                # Log overwrite
                if os.path.exists(target_file_path):
                    logging.warning(f"Overwriting existing file: {target_file_path}")

                try:
                    if dry_run:
                        logging.info(f"[Dry Run] Would copy: {source_file_path} -> {target_file_path}")
                    else:
                        shutil.copy2(source_file_path, target_file_path)
                        logging.info(f"Copied: {source_file_path} -> {target_file_path}")
                except Exception as e:
                    logging.error(f"Failed to copy '{source_file_path}' to '{target_file_path}': {e}")

    # --- Step 2: 중복 파일 제거 ---
    logging.info("--- Checking for duplicate posts ---")
    remove_duplicate_posts(source_dir, target_posts_dir, dry_run=dry_run)

    logging.info("Sync operation completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='블로그 포스트 동기화 및 중복 제거')
    parser.add_argument('--source-dir', type=str, default=None,
                        help='소스 디렉토리 경로 (기본값: _scripts/_posts)')
    parser.add_argument('--target-dir', type=str, default=None,
                        help='대상 레포 디렉토리 경로 (기본값: 자동 감지)')
    parser.add_argument('--dry-run', action='store_true',
                        help='실제 파일 작업 없이 계획만 출력')
    args = parser.parse_args()

    sync_posts(
        source_dir=args.source_dir,
        target_repo_dir=args.target_dir,
        dry_run=args.dry_run,
    )
