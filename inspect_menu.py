from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://demoqa.com/menu', wait_until='load')
    page.wait_for_timeout(500)

    # Відкриваємо підменю
    page.locator('a:has-text("Main Item 2")').evaluate("""
        el => {
            const ul = el.nextElementSibling;
            if (ul && ul.tagName === 'UL') ul.style.display = 'block';
        }
    """)
    page.wait_for_timeout(200)

    ul = page.locator('#nav > li:nth-child(2) > ul')
    print('visible after open:', ul.is_visible())
    print('computed display after open:', page.evaluate(
        "getComputedStyle(document.querySelector('#nav > li:nth-child(2) > ul')).display"
    ))

    # Закриваємо
    page.evaluate("document.querySelectorAll('#nav ul ul').forEach(ul => ul.style.display = 'none')")
    page.wait_for_timeout(200)

    print('visible after close:', ul.is_visible())
    print('computed display after close:', page.evaluate(
        "getComputedStyle(document.querySelector('#nav > li:nth-child(2) > ul')).display"
    ))
    print('inline style after close:', page.evaluate(
        "document.querySelector('#nav > li:nth-child(2) > ul').style.display"
    ))

    browser.close()
