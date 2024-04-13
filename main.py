from playwright.sync_api import sync_playwright, Playwright
from rich import print
import json


def run(playwright: Playwright):
    start_url = 'https://www.bhphotovideo.com/c/buy/Mirrorless-Camera-Lenses/ci/17912/N/4196380428'
    chrome = playwright.chromium
    broswer = chrome.launch(headless=False)
    page = broswer.new_page()
    # 把圖片關掉，加快網頁載入
    page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
    page.goto(start_url)
    times = 0

    while True:
        # detail pages
        for link in page.locator(
            "a[data-selenium='miniProductPageProductNameLink']"
        ).all():
            p = broswer.new_page(base_url='https://www.bhphotovideo.com/')
            p.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
            url = link.get_attribute('href')
            # 把圖片關掉，加快網頁載入
            if url is not None:
                p.goto(url)
            else:
                p.close()
            data = p.locator(
                "script[type='application/ld+json']").text_content()
            json_data = json.loads(data)
            print(json_data['name'])

            p.close()

        # 設定打開60頁就好
        if times == 59:
            # print(f"已經打開{times+1}pages")
            break
        else:
            page.locator("a[data-selenium='listingPagingPageNext']").click()
            times += 1
            # print(f"第{times}pages完畢")
    broswer.close()


with sync_playwright() as playwright:
    run(playwright)
