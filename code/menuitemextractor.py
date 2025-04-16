try:
    from code.menuitem import MenuItem
except ImportError:
    from menuitem import MenuItem


def clean_price(price: str) -> float:
    if not isinstance(price, str):
        price = str(price)
    price = price.replace('$', '').replace(',', '').strip()
    try:
        return float(price)
    except ValueError:
        return 0.0


def clean_scraped_text(scraped_text: str) -> list[str]:
    lines = scraped_text.split('\n')
    unwanted = {'', 'NEW!', 'NEW', 'S', 'V', 'GS', 'P'}
    return [line.strip() for line in lines if line.strip() not in unwanted]


def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    cleaned = clean_scraped_text(scraped_text)
    if len(cleaned) < 2:
        raise ValueError("Not enough information to extract menu item.")
    name = cleaned[0]
    price = clean_price(cleaned[1])
    description = cleaned[2] if len(cleaned) > 2 else "No description available"
    return MenuItem(
        category=title.strip(),
        name=name,
        price=price,
        description=description
    )


if __name__ == '__main__':
    raw_text = "\nNEW!\nTully Tots\n$11.79\nMade from scratch with shredded potatoes..."
    item = extract_menu_item("Starters", raw_text)
    print(item)
