import argparse
import hashlib
import json
import os
import re
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests  # (사용하지 않으면 제거 가능)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# HTML -> Markdown 변환 라이브러리
try:
    from markdownify import markdownify as md
except ImportError:
    # 설치가 안 되어 있다면, pip install markdownify
    def md(x):
        return x  # fallback - 그대로 반환

# --- 경로 상수 ---
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
_CSV_PATH = os.path.join(_REPO_ROOT, 'processed_posts.csv')


def compute_content_hash(content):
    """본문 내용의 MD5 해시를 계산합니다. 변경 감지용."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def escape_currency_dollars(content):
    """
    $숫자 패턴(통화 표기)만 \\$숫자로 이스케이프
    수식 $...$, $$...$$ 는 건드리지 않음

    예시:
    - "$100" -> "\\$100"
    - "$1,000.50" -> "\\$1,000.50"
    - "$x + y$" -> "$x + y$" (수식은 그대로)
    - "$$E=mc^2$$" -> "$$E=mc^2$$" (블록 수식은 그대로)
    """
    # $숫자 또는 $, (쉼표 포함 숫자) 패턴만 이스케이프
    # (?<!\$) - 앞에 $가 없어야 함 ($$는 제외)
    # (?=[\d,]) - 뒤에 숫자나 쉼표가 와야 함
    return re.sub(r'(?<!\$)\$(?=[\d,])', r'\\$', content)


def load_config():
    """설정 파일에서 설정값을 로드합니다."""
    config_path = os.path.join(_SCRIPT_DIR, 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_date_string(date_string: str) -> datetime.date:
    """
    Velog 글 목록 또는 상세 페이지에 표시되는 날짜 문자열을 실제 date 객체로 변환합니다.
    - '어제' => 오늘 - 1
    - '오늘' => 오늘
    - '2일 전' => 오늘 - 2
    - '2024년 12월 14일' => date(2024, 12, 14)
    등등을 처리합니다.
    """
    today = datetime.now().date()

    # 1) "N일 전", "어제", "오늘" 처리
    if '일 전' in date_string:
        try:
            days_ago = int(date_string.replace('일 전', '').strip())
            return today - timedelta(days=days_ago)
        except:
            return today
    elif '어제' in date_string:
        return today - timedelta(days=1)
    elif '오늘' in date_string:
        return today

    # 2) "YYYY년 MM월 DD일"
    try:
        temp = (date_string
                .replace('년', ' ')
                .replace('월', ' ')
                .replace('일', ' ')
                .strip())
        # "2024 12 14" -> 분리
        year, month, day = temp.split()
        year, month, day = int(year), int(month), int(day)
        return datetime(year, month, day).date()
    except:
        return today


def _chrome_options():
    """CI/로컬 공용 Chrome 옵션을 생성합니다."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return options


def get_post_links(username):
    """
    Velog 사용자의 모든 게시글 링크를 가져옵니다.

    Args:
        username (str): Velog 사용자명

    Returns:
        list: 게시글 URL 목록
    """
    url = f'https://velog.io/@{username}'

    # ChromeDriver 설정
    service = Service(ChromeDriverManager().install())
    options = _chrome_options()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    # 스크롤하여 모든 게시글 로드
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # 게시글 링크 추출
    links = []
    # (Velog UI가 바뀔 수 있으므로, a_tag의 class는 꼭 실제로 확인 필요)
    # 아래는 예시로 'a[class*="FlatPostCard_postThumbnail"]' 형태를 찾음
    for a_tag in soup.select('a[class*="FlatPostCard_postThumbnail"]'):
        href = a_tag.get('href')
        if href:
            # velog.io/@username/포스트-슬러그
            # 혹은 절대경로 href가 들어있을 수도 있으니 정규화 필요
            if href.startswith('/@'):
                # 절대경로로 만들기
                full_url = "https://velog.io" + href
                links.append(full_url)
            else:
                links.append(href)

    return links


def get_post_content(url):
    """
    개별 게시글의 내용을 가져옵니다.

    Args:
        url (str): 게시글 URL

    Returns:
        dict: 게시글 정보 (title, content, url, tags, date, year)
    """
    service = Service(ChromeDriverManager().install())
    options = _chrome_options()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # --------------------------------------------------------------------------------
        # (1) 제목 추출
        # --------------------------------------------------------------------------------
        title = None
        # head-wrapper 안에 있는 h1이 가장 정확
        head_wrapper = soup.find('div', class_='head-wrapper')
        if head_wrapper:
            h1_tag = head_wrapper.find('h1')
            if h1_tag:
                title = h1_tag.get_text(strip=True)

        # 그래도 없다면 select_one('.head-wrapper h1') 시도
        if not title:
            candidate = soup.select_one('.head-wrapper h1')
            if candidate:
                title = candidate.get_text(strip=True)

        if not title:
            title = "제목 없음"

        # --------------------------------------------------------------------------------
        # (2) 본문(HTML) -> markdown 변환
        # --------------------------------------------------------------------------------
        # 실제 Velog HTML 구조를 확인해서 가장 큰 본문 div를 찾으면 됩니다.
        # 예시: <div class="sc-dFtzxp bfzjcP"><div class="sc-bXTejn FTZwa"><div class="sc-eGRUor gdnhbG atom-one">
        content_div = soup.find('div', class_='sc-dFtzxp bfzjcP')
        if not content_div:
            # fallback
            content_div = soup.find('div', class_='sc-eGRUor')
        if not content_div:
            # fallback
            content_div = soup.select_one('.atom-one')

        if content_div:
            html_content = str(content_div)
            markdown_content = md(html_content)
        else:
            markdown_content = "내용 없음"

        # --------------------------------------------------------------------------------
        # (3) 날짜 추출
        # --------------------------------------------------------------------------------
        # Velog 상세 페이지의 경우 <div class="information"><span>3일 전</span>...</div> 형태일 수 있음
        # 아래는 예시로 "information" div 안의 span 중 마지막(날짜) 텍스트를 가져온다고 가정
        info_div = soup.find('div', class_='information')
        if info_div:
            all_spans = info_div.find_all('span')
            if len(all_spans) >= 1:
                # 예: 3일 전 / 2024년 12월 14일 / ...
                date_str = all_spans[-1].get_text(strip=True)
            else:
                date_str = "오늘"
        else:
            # 상세 페이지에 날짜 표시가 없을 수도 있으니, 그냥 "오늘"로 처리
            date_str = "오늘"

        post_date = parse_date_string(date_str)
        year_str = str(post_date.year)

        # --------------------------------------------------------------------------------
        # (4) 태그 추출
        # --------------------------------------------------------------------------------
        # 예시: <div class="sc-cZMNgc bpMcZw"><a href="/tags/IT지식">IT지식</a> ...</div>
        tags = []
        tag_wrapper = soup.find('div', class_='sc-cZMNgc bpMcZw')
        if tag_wrapper:
            for a_tag in tag_wrapper.find_all('a'):
                tag_text = a_tag.get_text(strip=True)
                if tag_text:
                    tags.append(tag_text)

        return {
            'title': title,
            'content': markdown_content,
            'url': url,
            'tags': tags,
            'date': post_date.strftime('%Y-%m-%d'),  # "YYYY-MM-DD"
            'year': year_str
        }
    finally:
        driver.quit()


def save_as_markdown(post, base_output_dir):
    """
    게시글을 마크다운 파일로 저장합니다.
    base_output_dir 아래에 연도(year)별 폴더를 만들어 저장.
    예: _posts/2024/2024-12-22-제목.md
    """
    # year별 폴더 생성
    output_dir = os.path.join(base_output_dir, post['year'])
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 파일명: "YYYY-MM-DD-제목.md"
    safe_title = post['title']

    # (1) & -> and 변환 (Sitemap XML 에러 방지)
    safe_title = safe_title.replace('&', 'and')

    # (2) 파일명에 들어가면 안 되는 문자 모두 치환
    invalid_chars = '<>:"|?*·/\\\'\r\n\t'
    for ch in invalid_chars:
        safe_title = safe_title.replace(ch, '_')

    # (3) 연속된 '__' -> '_'
    while '__' in safe_title:
        safe_title = safe_title.replace('__', '_')

    # (4) 너무 긴 제목은 잘라서 사용 (파일시스템 대응)
    if len(safe_title) > 200:
        safe_title = safe_title[:197] + '...'

    file_name = f"{post['date']}-{safe_title}.md"
    filepath = os.path.join(output_dir, file_name)
    print(f"[Saving Post] {filepath}")

    # YAML Front Matter + 본문 작성
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f"title: \"{post['title']}\"\n")
        f.write(f"date: \"{post['date']}\"\n")
        if post.get('tags'):
            f.write("tags:\n")
            for tg in post['tags']:
                f.write(f"  - \"{tg}\"\n")
        f.write(f"year: \"{post['year']}\"\n")
        f.write("---\n\n")

        # 제목 / 원본 링크
        f.write(f"# {post['title']}\n\n")
        # f.write(f"원본 게시글: {post['url']}\n\n")

        # 마크다운 변환된 본문 (통화 $ 이스케이프 적용)
        escaped_content = escape_currency_dollars(post['content'])
        f.write(escaped_content)

    # 환경 간 이식성을 위해 레포 루트 기준 상대 경로 반환
    return os.path.relpath(filepath, _REPO_ROOT)


def _resolve_file_path(rel_path):
    """CSV에 저장된 상대 경로를 절대 경로로 복원합니다."""
    if not rel_path:
        return ''
    if os.path.isabs(rel_path):
        # 레거시 절대 경로 호환: 파일명만 추출하여 _posts/ 아래에서 탐색
        return rel_path
    return os.path.join(_REPO_ROOT, rel_path)


def load_processed_posts_df():
    """processed_posts.csv를 DataFrame으로 로드합니다."""
    if os.path.exists(_CSV_PATH):
        df = pd.read_csv(_CSV_PATH)
        # 기존 CSV 호환: 새 컬럼이 없으면 빈값으로 추가
        for col in ['content_hash', 'file_path']:
            if col not in df.columns:
                df[col] = ''
        return df
    return pd.DataFrame(columns=['url', 'title', 'status', 'processed_at', 'content_hash', 'file_path'])


def load_processed_posts():
    """이미 처리된 게시글 URL set을 로드합니다 (하위 호환)."""
    df = load_processed_posts_df()
    return set(df['url'].tolist())


def load_processed_posts_dict():
    """URL -> {title, status, content_hash, file_path, processed_at} 딕셔너리로 로드합니다."""
    df = load_processed_posts_df()
    result = {}
    for _, row in df.iterrows():
        result[row['url']] = {
            'title': row.get('title', ''),
            'status': row.get('status', ''),
            'content_hash': row.get('content_hash', ''),
            'file_path': row.get('file_path', ''),
            'processed_at': row.get('processed_at', '')
        }
    return result


def save_processed_post(url, title, status='success', content_hash='', file_path=''):
    """처리된 게시글 정보를 CSV에 저장(upsert — URL 중복 시 기존 행 갱신)."""
    now = pd.Timestamp.now()

    if os.path.exists(_CSV_PATH):
        df = load_processed_posts_df()
        mask = df['url'] == url
        if mask.any():
            # 기존 행 갱신 (upsert)
            df.loc[mask, 'title'] = title
            df.loc[mask, 'status'] = status
            df.loc[mask, 'processed_at'] = now
            df.loc[mask, 'content_hash'] = content_hash
            df.loc[mask, 'file_path'] = file_path
        else:
            new_row = pd.DataFrame({
                'url': [url], 'title': [title], 'status': [status],
                'processed_at': [now], 'content_hash': [content_hash],
                'file_path': [file_path]
            })
            df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = pd.DataFrame({
            'url': [url], 'title': [title], 'status': [status],
            'processed_at': [now], 'content_hash': [content_hash],
            'file_path': [file_path]
        })

    df.to_csv(_CSV_PATH, index=False)


def update_processed_post(url, title=None, status=None, content_hash=None, file_path=None):
    """기존 CSV 레코드를 업데이트합니다."""
    df = load_processed_posts_df()
    mask = df['url'] == url
    if not mask.any():
        return False
    if title is not None:
        df.loc[mask, 'title'] = title
    if status is not None:
        df.loc[mask, 'status'] = status
    if content_hash is not None:
        df.loc[mask, 'content_hash'] = content_hash
    if file_path is not None:
        df.loc[mask, 'file_path'] = file_path
    df.loc[mask, 'processed_at'] = pd.Timestamp.now()
    df.to_csv(_CSV_PATH, index=False)
    return True


def check_existing_post(title, base_output_dir, year):
    """이미 동일 제목 파일이 존재하는지 여부를 확인합니다."""
    output_dir = os.path.join(base_output_dir, year)
    if not os.path.exists(output_dir):
        return False
    for filename in os.listdir(output_dir):
        if filename.endswith('.md'):
            # 파일명 안에 title이 들어있다면 이미 저장했다고 간주
            if title in filename:
                return True
    return False


def log_error(url, error_message):
    """
    오류 발생 시 별도의 로그 파일(error_logs.txt)에 기록합니다.
    """
    with open(os.path.join(_REPO_ROOT, 'error_logs.txt'), 'a', encoding='utf-8') as f:
        f.write(f"[ERROR] URL: {url}\n")
        f.write(f"        Error: {error_message}\n\n")


def crawl_new_posts(username, base_output_dir):
    """새로운 포스트만 크롤링합니다 (기본 모드)."""
    processed_urls = load_processed_posts()

    print("게시글 링크 수집 중...")
    post_links = get_post_links(username)
    new_links = [url for url in post_links if url not in processed_urls]

    if not new_links:
        print("새로운 게시글이 없습니다.")
        return post_links

    print(f"총 {len(new_links)}개의 새로운 게시글을 처리합니다...")

    for url in new_links:
        try:
            post = get_post_content(url)

            if check_existing_post(post['title'], base_output_dir, post['year']):
                print(f"[중복] 이미 저장된 게시글: {post['title']}")
                save_processed_post(url, post['title'], 'skipped')
                continue

            filepath = save_as_markdown(post, base_output_dir)
            content_hash = compute_content_hash(post['content'])
            save_processed_post(url, post['title'], 'success', content_hash, filepath)
            print(f"[완료] 저장: {post['title']}")
            time.sleep(1)

        except Exception as e:
            error_message = f"[ERROR] URL: {url}\n        Error: {str(e)}\n\n"
            print(error_message)
            with open(os.path.join(_REPO_ROOT, 'error_log.txt'), 'a', encoding='utf-8') as f:
                f.write(error_message)
            continue

    return post_links


def check_updates(username, base_output_dir, post_links=None):
    """이미 크롤링한 포스트 중 업데이트된 것을 감지하고 다시 저장합니다."""
    processed = load_processed_posts_dict()

    if not processed:
        print("처리된 포스트가 없습니다. 먼저 기본 크롤링을 실행하세요.")
        return

    # 이미 수집된 링크가 있으면 재활용, 없으면 새로 수집
    if post_links is None:
        print("게시글 링크 수집 중...")
        post_links = get_post_links(username)

    # success 상태인 것만 업데이트 체크 (skipped, archived 제외)
    urls_to_check = [url for url in post_links if url in processed and processed[url]['status'] == 'success']

    if not urls_to_check:
        print("업데이트를 확인할 포스트가 없습니다.")
        return

    print(f"총 {len(urls_to_check)}개의 기존 포스트 업데이트 확인 중...")
    updated_count = 0

    for url in urls_to_check:
        try:
            post = get_post_content(url)
            new_hash = compute_content_hash(post['content'])
            old_hash = processed[url].get('content_hash', '')

            if old_hash and new_hash == old_hash:
                print(f"[변경없음] {post['title']}")
                time.sleep(1)
                continue

            # 기존 파일이 있으면 삭제 후 새로 저장
            old_file = _resolve_file_path(processed[url].get('file_path', ''))
            if old_file and os.path.exists(old_file):
                os.remove(old_file)
                print(f"[삭제] 기존 파일: {old_file}")

            rel_path = save_as_markdown(post, base_output_dir)
            update_processed_post(url, title=post['title'], status='success',
                                  content_hash=new_hash, file_path=rel_path)
            updated_count += 1
            print(f"[업데이트] {post['title']}")
            time.sleep(1)

        except Exception as e:
            error_message = f"[ERROR] 업데이트 확인 중 - URL: {url}\n        Error: {str(e)}\n\n"
            print(error_message)
            with open(os.path.join(_REPO_ROOT, 'error_log.txt'), 'a', encoding='utf-8') as f:
                f.write(error_message)
            continue

    print(f"\n업데이트 완료: {updated_count}개 포스트 갱신됨")


def sync_deletions(username, base_output_dir, post_links=None):
    """Velog에서 삭제된 포스트를 감지하고 로컬에서 archive 처리합니다."""
    processed = load_processed_posts_dict()

    if not processed:
        print("처리된 포스트가 없습니다.")
        return

    if post_links is None:
        print("게시글 링크 수집 중...")
        post_links = get_post_links(username)

    current_urls = set(post_links)
    # success 상태인데 현재 Velog에 없는 URL = 삭제된 포스트
    deleted_urls = [url for url in processed
                    if url not in current_urls and processed[url]['status'] == 'success']

    if not deleted_urls:
        print("삭제된 포스트가 없습니다.")
        return

    print(f"총 {len(deleted_urls)}개의 삭제된 포스트를 감지했습니다.")

    archive_dir = os.path.join(base_output_dir, '_archived')
    Path(archive_dir).mkdir(parents=True, exist_ok=True)

    archived_count = 0
    for url in deleted_urls:
        info = processed[url]
        old_file = _resolve_file_path(info.get('file_path', ''))

        if old_file and os.path.exists(old_file):
            # _archived/ 폴더로 이동
            dest = os.path.join(archive_dir, os.path.basename(old_file))
            shutil.move(old_file, dest)
            rel_dest = os.path.relpath(dest, _REPO_ROOT)
            update_processed_post(url, status='archived', file_path=rel_dest)
            archived_count += 1
            print(f"[아카이브] {info.get('title', url)} -> {dest}")
        else:
            # 파일은 없지만 CSV 상태만 업데이트
            update_processed_post(url, status='archived')
            print(f"[아카이브] {info.get('title', url)} (파일 없음, 상태만 변경)")

    print(f"\n아카이브 완료: {archived_count}개 파일 이동됨")


def crawl_and_save_posts(check_updates_flag=False, sync_deletions_flag=False):
    config = load_config()
    username = config['velog_username']

    base_output_dir = os.path.join(_REPO_ROOT, '_posts')
    Path(base_output_dir).mkdir(parents=True, exist_ok=True)

    # (1) 항상 새 포스트 크롤링 먼저 실행
    post_links = crawl_new_posts(username, base_output_dir)

    # (2) 업데이트 확인 모드
    if check_updates_flag:
        print("\n--- 업데이트 확인 모드 ---")
        check_updates(username, base_output_dir, post_links)

    # (3) 삭제 동기화 모드
    if sync_deletions_flag:
        print("\n--- 삭제 동기화 모드 ---")
        sync_deletions(username, base_output_dir, post_links)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Velog 블로그 크롤러')
    parser.add_argument('--check-updates', action='store_true',
                        help='기존 포스트의 업데이트 여부를 확인하고 갱신합니다')
    parser.add_argument('--sync-deletions', action='store_true',
                        help='Velog에서 삭제된 포스트를 로컬에서 아카이브합니다')
    parser.add_argument('--full-sync', action='store_true',
                        help='업데이트 확인 + 삭제 동기화를 모두 수행합니다')
    args = parser.parse_args()

    do_updates = args.check_updates or args.full_sync
    do_deletions = args.sync_deletions or args.full_sync

    crawl_and_save_posts(check_updates_flag=do_updates, sync_deletions_flag=do_deletions)
