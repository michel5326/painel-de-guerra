import random

MAX_CALLOUT = 25


def safe_text(text, limit):
    text = text.strip()

    if len(text) <= limit:
        return text

    return text[:limit].strip()


CALLOUTS_PT = [
    "Frete Grátis",
    "Compra 100% Segura",
    "Produto Original",
    "Entrega Rápida",
    "90 Dias de Garantia",
    "Promoção Especial",
    "Desconto Exclusivo",
    "Oferta por Tempo Limitado",
    "Site Oficial",
    "Garantia de Satisfação",
    "Envio Imediato",
    "Estoque Limitado"
]


CALLOUTS_EN = [
    "Free Shipping",
    "100% Secure Checkout",
    "Original Product",
    "Fast Delivery",
    "90 Day Guarantee",
    "Special Promotion",
    "Exclusive Discount",
    "Limited Time Offer",
    "Official Website",
    "Money Back Guarantee",
    "Immediate Shipping",
    "Limited Stock"
]


def generate_callouts(country):

    templates = CALLOUTS_PT if country == "BR" else CALLOUTS_EN

    templates = templates.copy()
    random.shuffle(templates)

    callouts = []

    for c in templates:

        callout = safe_text(c, MAX_CALLOUT)

        if callout and callout not in callouts:
            callouts.append(callout)

    return callouts[:10]