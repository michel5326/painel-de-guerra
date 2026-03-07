def generate_keywords(product_name):

    product = product_name.lower()

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
        f"{product} before and after",
        f"{product} customer reviews"
    ]

    transactional_keywords = [
        f"buy {product}",
        f"order {product}",
        f"{product} price",
        f"{product} discount",
        f"{product} official offer",
        f"{product} shop",
        f"{product} buy online",
        f"{product} best price",
        f"{product} where to buy"
    ]

    return {
        "brand": brand_keywords,
        "commercial": commercial_keywords,
        "transactional": transactional_keywords
    }