from playwright.sync_api import sync_playwright, Playwright
from menuitemextractor import extract_menu_item
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Use archived URL
    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")
    page.wait_for_timeout(3000)

    titles = page.locator(".menu-category-title")
    section_count = titles.count()
    print(f"Found {section_count} section titles.")

    items_list = []

    for i in range(section_count):
        try:
            title = titles.nth(i).inner_text()
            print(f"\n--- Section: {title} ---")

            section = titles.nth(i).locator("..").locator("..").locator(".row")
            menu_items = section.locator(".menu-item")
            item_count = menu_items.count()

            print(f"Found {item_count} items.")

            for j in range(item_count):
                try:
                    raw_text = menu_items.nth(j).inner_text()
                    print(f"\nRaw text:\n{raw_text}")
                    menu_item = extract_menu_item(title, raw_text)
                    item_dict = menu_item.to_dict()
                    print("Parsed:", item_dict)
                    items_list.append(item_dict)
                except Exception as e:
                    print("❌ Parse Error:", e)
        except Exception as sec_e:
            print("❌ Section Error:", sec_e)

    print(f"\n✅ Scraped total items: {len(items_list)}")

    # Save to CSV
    if len(items_list) > 0:
        df = pd.DataFrame(items_list)
        df.to_csv("cache/tullys_menu.csv", index=False)
        print("📁 CSV saved successfully.")
    else:
        print("⚠️ No items scraped. CSV not saved.")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        tullyscraper(playwright)

