MAX_DESCRIPTION = 90


def safe_text(text, limit):
    text = text.strip()

    if len(text) <= limit:
        return text

    return text[:limit].strip()


DESCRIPTIONS_PT = [
    "Compre {product} hoje por apenas R${price}. Oferta especial disponível.",
    "Economize R${discount} hoje. Peça {product} com compra segura.",
    "Frete grátis disponível. Receba {product} com entrega rápida.",
    "Aproveite a oferta oficial de {product} com estoque limitado."
]


DESCRIPTIONS_EN = [
    "Buy {product} today for only ${price}. Limited time offer.",
    "Save ${discount} today. Order {product} with secure checkout.",
    "Free shipping available. Get {product} with fast delivery.",
    "Official {product} offer with limited stock available."
]


def generate_descriptions(product_name, price, discount_value, country):

    product_name = product_name.title()

    templates = DESCRIPTIONS_PT if country == "BR" else DESCRIPTIONS_EN

    descriptions = []

    price = int(price) if price else 0
    discount = int(discount_value) if discount_value else 0

    for template in templates:

        description = template

        description = description.replace("{product}", product_name)
        description = description.replace("{price}", str(price))
        description = description.replace("{discount}", str(discount))

        description = safe_text(description, MAX_DESCRIPTION)

        if description not in descriptions:
            descriptions.append(description)

    return descriptions[:4]