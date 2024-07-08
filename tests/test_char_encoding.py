# test_char_encoding.py
import pytest
from playwright.sync_api import sync_playwright
from chardet import detect

def detect_garbled_text(text):
    garbled_patterns = ["�", "���", "�", "\ufffd"]
    for pattern in garbled_patterns:
        if pattern in text:
            return True
    return False

def detect_encoding(content):
    result = detect(content)
    return result['encoding']

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.parametrize("url", [
    "https://www.ptw.inc/",
    "https://qiita.com/KTakahiro1729/items/88f1da528b42f2740d14",
])
def test_no_garbled_text(browser, url):
    page = browser.new_page()
    page.goto(url)
    content = page.content().encode('utf-8')
    page.close()
    
    encoding = detect_encoding(content)
    
    is_garbled = detect_garbled_text(content.decode('utf-8', errors='replace'))
    
    with open("garbled_report.txt", "a", encoding="utf-8") as report_file:
        report_file.write(f"URL: {url}\n")
        report_file.write(f"Encoding: {encoding}\n")
        report_file.write(f"Garbled: {'Yes' if is_garbled else 'No'}\n")
        report_file.write("\n")

    assert not is_garbled, f"文字化けが検出されました: {url}"

if __name__ == "__main__":
    pytest.main(["-v", "test_char_encoding.py"])
