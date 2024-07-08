# test_char_encoding.py
import pytest
from playwright.sync_api import sync_playwright

def detect_garbled_text(text):
    # 簡単な文字化け検出ロジック
    # ここでは例として、意味不明な文字列パターンを簡単にチェックする
    # 必要に応じて複雑なロジックに変更
    garbled_patterns = ["�", "���", "�", "\ufffd"]
    for pattern in garbled_patterns:
        if pattern in text:
            return True
    return False

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.parametrize("url", [
    "https://www.ptw.inc/",
    "https://qiita.com/KTakahiro1729/items/88f1da528b42f2740d14",
    # 他のテストするURLをここに追加
])
def test_no_garbled_text(browser, url):
    page = browser.new_page()
    page.goto(url)
    content = page.content()
    page.close()
    
    assert not detect_garbled_text(content), f"文字化けが検出されました: {url}"

if __name__ == "__main__":
    pytest.main(["-v", "test_char_encoding.py"])
