import os
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv

load_dotenv()

def search_google_api(query):
    """
    Google Custom Search APIを使用して検索を行う関数
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

    if not api_key or not cse_id:
        raise ValueError("環境変数 GOOGLE_API_KEY と CUSTOM_SEARCH_ENGINE_ID が設定されていません。")

    service = build("customsearch", "v1", developerKey=api_key)

    try:
        res = service.cse().list(q=query, cx=cse_id).execute()
        search_results = []
        if 'items' in res:
            for item in res['items']:
                search_result = {
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                }
                search_results.append(search_result)
        return search_results
    except Exception as e:
        print(f"Google Custom Search API エラー: {e}")
        return []

def fetch_site_content(url):
    """
    指定されたURLのサイト内容をfetchする関数
    """
    try:
        response = requests.get(url, timeout=10)  # タイムアウト設定
        response.raise_for_status()  # HTTPエラーをチェック

        soup = BeautifulSoup(response.content, 'html.parser')

        # 不要なタグを除去 (スクリプト、スタイル、広告、ナビゲーションなど)
        for tag in soup(["script", "style", "aside", "nav", "footer", "header", "form", "iframe", "noscript", "svg", "canvas", "input", "button", "select", "textarea", "dialog", "menu", "menuitem", "object", "embed", "applet", "bgsound", "blink", "marquee", "noembed", "noframes", "param", "portal", "rb", "rtc", "script", "shadow", "slot", "spacer", "strike", "tt", "xmp"]):
            tag.extract()

        # meta, link, style タグも除去
        for tag_name in ['meta', 'link', 'style']:
            for tag in soup.find_all(tag_name):
                tag.extract()


        # テキストを取得 (改行と空白を調整)
        text_content = soup.get_text(separator='\n', strip=True)

        return text_content

    except requests.exceptions.RequestException as e:
        print(f"URL {url} の取得エラー: {e}")
        return ""
    except Exception as e:
        print(f"URL {url} のコンテンツ処理エラー: {e}")
        return ""
