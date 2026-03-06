from .blocks.headlines import generate_headlines
from .blocks.descriptions import generate_descriptions
from .blocks.callouts import generate_callouts
from .keywords.keywords import generate_keywords


class CampaignGeneratorService:

    def generate_campaign_structure(self, product_name, price, discount_value, discount_percent, country):

        product_name = product_name.title()

        headlines = generate_headlines(
            product_name,
            price,
            discount_value,
            discount_percent,
            country
        )

        descriptions = generate_descriptions(
            product_name,
            price,
            discount_value,
            country
        )

        callouts = generate_callouts(country)

        keywords = generate_keywords(product_name)

        campaigns = [

            {
                "campaign_name": f"Search | {product_name} | Brand",
                "ad_group": f"{product_name} Brand",
                "keywords": keywords["brand"],
                "ads": {
                    "headlines": headlines["brand"],
                    "descriptions": descriptions
                },
                "callouts": callouts
            },

            {
                "campaign_name": f"Search | {product_name} | Commercial",
                "ad_group": f"{product_name} Reviews",
                "keywords": keywords["commercial"],
                "ads": {
                    "headlines": headlines["commercial"],
                    "descriptions": descriptions
                },
                "callouts": callouts
            },

            {
                "campaign_name": f"Search | {product_name} | Transactional",
                "ad_group": f"Buy {product_name}",
                "keywords": keywords["transactional"],
                "ads": {
                    "headlines": headlines["transactional"],
                    "descriptions": descriptions
                },
                "callouts": callouts
            }

        ]

        return campaigns