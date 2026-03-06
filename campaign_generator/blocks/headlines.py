from .headline_templates import HEADLINES_PT, HEADLINES_EN
from .headline_builder import build_headlines


def generate_headlines(product_name, price, discount_value, discount_percent, country):

    product_name = product_name.title()

    price = int(price) if price else 0
    discount = int(discount_value) if discount_value else 0
    discount_percent = int(discount_percent) if discount_percent else 0

    templates = HEADLINES_PT if country == "BR" else HEADLINES_EN

    return {
        "brand": build_headlines(
            templates["brand"], product_name, price, discount, discount_percent
        )[:15],

        "commercial": build_headlines(
            templates["commercial"], product_name, price, discount, discount_percent
        )[:15],

        "transactional": build_headlines(
            templates["transactional"], product_name, price, discount, discount_percent
        )[:15]
    }