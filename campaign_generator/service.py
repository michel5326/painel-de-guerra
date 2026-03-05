from .templates import headlines_en, headlines_pt, descriptions_en, descriptions_pt


MAX_HEADLINE = 30
MAX_DESCRIPTION = 90


def safe_text(text, limit):
    text = text.strip()

    if len(text) <= limit:
        return text

    return text[:limit].strip()


class CampaignGeneratorService:

    def generate_headlines(self, product_name, price, discount_value, discount_percent, country):

        product_name = product_name.title()

        templates = headlines_pt if country == "BR" else headlines_en

        headlines = []

        price = int(price) if price else 0
        discount = int(discount_value) if discount_value else 0
        discount_percent = int(discount_percent) if discount_percent else 0

        for template in templates:

            headline = template

            headline = headline.replace("{product}", product_name)
            headline = headline.replace("{price}", str(price))
            headline = headline.replace("{discount}", str(discount))
            headline = headline.replace("{discount_percent}", str(discount_percent))

            headline = safe_text(headline, MAX_HEADLINE)

            if headline and headline not in headlines:
                headlines.append(headline)

        return headlines[:15]


    def generate_descriptions(self, product_name, price, discount_value, country):

        product_name = product_name.title()

        templates = descriptions_pt if country == "BR" else descriptions_en

        descriptions = []

        price = int(price) if price else 0
        discount = int(discount_value) if discount_value else 0

        for template in templates:

            description = template

            description = description.replace("{product}", product_name)
            description = description.replace("{price}", str(price))
            description = description.replace("{discount}", str(discount))

            description = safe_text(description, MAX_DESCRIPTION)

            if description and description not in descriptions:
                descriptions.append(description)

        return descriptions[:4]


    def generate_keywords(self, product_name):

        product = product_name.lower()

        brand_keywords = [
            f"{product}",
            f"{product} official",
            f"{product} official website",
            f"{product} site"
        ]

        commercial_keywords = [
            f"{product} reviews",
            f"{product} review",
            f"{product} results",
            f"{product} complaints",
            f"{product} does it work"
        ]

        transactional_keywords = [
            f"buy {product}",
            f"order {product}",
            f"{product} price",
            f"{product} discount",
            f"{product} official offer",
            f"{product} shop"
        ]

        return {
            "brand": brand_keywords,
            "commercial": commercial_keywords,
            "transactional": transactional_keywords
        }


    def generate_campaign_structure(self, product_name, price, discount_value, discount_percent, country):

        product_name = product_name.title()

        headlines = self.generate_headlines(
            product_name,
            price,
            discount_value,
            discount_percent,
            country
        )

        descriptions = self.generate_descriptions(
            product_name,
            price,
            discount_value,
            country
        )

        keywords = self.generate_keywords(product_name)

        campaigns = [

            {
                "campaign_name": f"Search | {product_name} | Brand",
                "ad_group": f"{product_name} Brand",
                "keywords": keywords["brand"],
                "ads": {
                    "headlines": headlines,
                    "descriptions": descriptions
                }
            },

            {
                "campaign_name": f"Search | {product_name} | Commercial",
                "ad_group": f"{product_name} Reviews",
                "keywords": keywords["commercial"],
                "ads": {
                    "headlines": headlines,
                    "descriptions": descriptions
                }
            },

            {
                "campaign_name": f"Search | {product_name} | Transactional",
                "ad_group": f"Buy {product_name}",
                "keywords": keywords["transactional"],
                "ads": {
                    "headlines": headlines,
                    "descriptions": descriptions
                }
            }

        ]

        return campaigns