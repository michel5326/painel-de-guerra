def generate_keywords(product_name, country="US"):

    product = product_name.lower()

    if country == "BR":

        brand_keywords = [
            f"{product}",
            f"{product} oficial",
            f"{product} site oficial",
            f"{product} site",
            f"{product} original"
        ]

        commercial_keywords = [
            f"{product} funciona",
            f"{product} vale a pena",
            f"{product} avaliações",
            f"{product} resultados",
            f"{product} reclamações",
            f"{product} antes e depois"
        ]

        transactional_keywords = [
            f"comprar {product}",
            f"{product} preço",
            f"{product} desconto",
            f"{product} promoção",
            f"{product} onde comprar",
            f"{product} comprar online"
        ]

    else:

        brand_keywords = [
            f"{product}",
            f"{product} official",
            f"{product} official website",
            f"{product} official site",
            f"{product} site",
            f"{product} original"
        ]

        commercial_keywords = [
            f"{product} reviews",
            f"{product} review",
            f"{product} results",
            f"{product} complaints",
            f"{product} does it work",
            f"{product} worth it",
            f"{product} before and after"
        ]

        transactional_keywords = [
            f"buy {product}",
            f"order {product}",
            f"{product} price",
            f"{product} discount",
            f"{product} official offer",
            f"{product} buy online",
            f"{product} best price",
            f"{product} where to buy"
        ]

    return {
        "brand": brand_keywords,
        "commercial": commercial_keywords,
        "transactional": transactional_keywords
    }