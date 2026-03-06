MAX_HEADLINE = 30


def safe_text(text, limit):

    text = text.strip()

    if len(text) <= limit:
        return text

    return text[:limit].strip()


def build_headlines(templates, product_name, price, discount, discount_percent):

    headlines = []

    for template in templates:

        headline = template

        headline = headline.replace("{product}", product_name)
        headline = headline.replace("{price}", str(price))
        headline = headline.replace("{discount}", str(discount))
        headline = headline.replace("{discount_percent}", str(discount_percent))

        headline = safe_text(headline, MAX_HEADLINE)

        if headline not in headlines:
            headlines.append(headline)

    return headlines