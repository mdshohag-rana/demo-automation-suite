from playwright.sync_api import Page, expect
import logging
import allure


def test_quotes_page_url(page: Page):
    page.goto("https://quotes.toscrape.com/")
    print("Current URL:", page.url)
    logging.info(f"Current URL: {page.url}")
    assert "https://quotes.toscrape.com/" == page.url

def test_quotes_page_title(page: Page):
    page.goto("https://quotes.toscrape.com/")
    assert "Quotes to Scrape" in page.title()

def test_quotes_content(page: Page):
    with allure.step("Open quotes website"):
        page.goto("https://quotes.toscrape.com/")

    with allure.step("Locate all quote elements"):
        quotes = page.locator("div.quote span.text")
        count = quotes.count()

    with allure.step(f"Validate total quotes count: {count}"):
        assert count > 0, f"Expected at least one quote, found {count}"

    for i in range(count):
        quote = quotes.nth(i)

        with allure.step(f"Validate quote {i + 1} is visible and not empty"):
            expect(quote).to_be_visible()

            text = quote.text_content()
            assert text and text.strip(), f"Quote {i+1} is empty"

    with allure.step("Validate first quote exists"):
        expect(quotes.first).to_be_visible()

def test_top_ten_tag_items(page: Page) -> None:
    page.goto("https://quotes.toscrape.com/")

    items = page.locator("span.tag-item a")

    expect(items).to_have_count(10)

    for i in range(items.count()):
        item = items.nth(i)

        expect(item).to_be_visible()

        tag = item.inner_text().strip()
        assert tag

        with allure.step(f"Validate tag {i+1}: {tag}"):
            with page.expect_navigation():
                item.click()

            assert tag in page.url
            print(f"PASS: {tag}")

        page.go_back()

def test_log_in(page: Page) -> None:
    page.goto("https://quotes.toscrape.com/login")

    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "testpassword")
    page.click("input[type='submit']")

    expect(page.locator("div.alert")).to_have_text("Invalid username or password")
    