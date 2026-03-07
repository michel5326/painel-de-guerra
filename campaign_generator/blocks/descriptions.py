MAX_DESCRIPTION = 90


def safe_text(text, limit):
    text = text.strip()

    if len(text) <= limit:
        return text

    return text[:limit].strip()


DESCRIPTIONS_PT = [

"Compre {product} com {shipping}. {guarantee_days} dias de garantia.",
"Garanta {product} hoje com {discount_percent}% de desconto. {shipping}.",
"Oferta oficial de {product}. Apenas R${price} por unidade. {shipping}.",
"Compre {product} agora com desconto exclusivo e entrega rápida."

]


DESCRIPTIONS_EN = [

"Buy {product} today with {shipping}. {guarantee_days}-day guarantee.",
"Get {product} now with {discount_percent}% discount. {shipping}.",
"Official {product} offer. Only ${price} per unit. {shipping}.",
"Order {product} today with exclusive discount and fast delivery."

]


def generate_descriptions(
    product_name,
    price,
    discount_percent,
    guarantee_days,
    free_shipping,
    country
):

    product_name = product_name.title()

    templates = DESCRIPTIONS_PT if country == "BR" else DESCRIPTIONS_EN

    descriptions = []

    price = int(price) if price else 0
    discount_percent = int(discount_percent) if discount_percent else 0
    guarantee_days = int(guarantee_days) if guarantee_days else 30

    if free_shipping:
        shipping = "frete grátis e entrega rápida" if country == "BR" else "free shipping and fast delivery"
    else:
        shipping = "entrega rápida" if country == "BR" else "fast delivery"

    for template in templates:

        description = template

        description = description.replace("{product}", product_name)
        description = description.replace("{price}", str(price))
        description = description.replace("{discount_percent}", str(discount_percent))
        description = description.replace("{guarantee_days}", str(guarantee_days))
        description = description.replace("{shipping}", shipping)

        description = safe_text(description, MAX_DESCRIPTION)

        if description not in descriptions:
            descriptions.append(description)

    return descriptions[:4]