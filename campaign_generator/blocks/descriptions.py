import random

MAX_DESCRIPTION = 90


def safe_text(text, limit):
    text = text.strip()

    if len(text) <= limit:
        return text

    return text[:limit].strip()


DESCRIPTIONS_PT = [
    "Compre {product} no site oficial por apenas R${price}. Oferta por tempo limitado.",
    "Economize R${discount} hoje. Pedido seguro de {product} com garantia.",
    "Frete grátis disponível. Receba {product} com entrega rápida.",
    "Oferta oficial de {product} com desconto especial hoje.",
    "Peça {product} agora com frete grátis e compra segura.",
    "Garanta {product} hoje com promoção e estoque limitado.",
    "Compre {product} com desconto especial e entrega rápida.",
    "Pedido oficial de {product} com garantia e envio imediato."
]


DESCRIPTIONS_EN = [
    "Buy {product} from the official website for only ${price}. Limited time offer.",
    "Save ${discount} today. Order {product} with secure checkout.",
    "Free shipping available. Get {product} with fast delivery.",
    "Official {product} offer with special discount today.",
    "Order {product} now with free shipping and secure checkout.",
    "Get {product} today with promotional price and limited stock.",
    "Buy {product} with discount and fast delivery available.",
    "Official {product} order with guarantee and quick shipping."
]


def generate_descriptions(product_name, price, discount_value, country):

    product_name = product_name.title()

    templates = DESCRIPTIONS_PT if country == "BR" else DESCRIPTIONS_EN

    price = int(price) if price else 0
    discount = int(discount_value) if discount_value else 0

    templates = templates.copy()
    random.shuffle(templates)

    descriptions = []

    for template in templates:

        description = template

        description = description.replace("{product}", product_name)
        description = description.replace("{price}", str(price))
        description = description.replace("{discount}", str(discount))

        description = safe_text(description, MAX_DESCRIPTION)

        if description and description not in descriptions:
            descriptions.append(description)

    return descriptions[:4]