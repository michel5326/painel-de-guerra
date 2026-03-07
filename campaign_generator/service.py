from .blocks.headlines import generate_headlines
from .blocks.descriptions import generate_descriptions
from .blocks.callouts import generate_callouts
from .keywords.keywords import generate_keywords


class CampaignGeneratorService:

    def generate_campaign_structure(
        self,
        product_name,
        price,
        discount_value,
        discount_percent,
        country,
        guarantee_days=None,
        installments_text=None,
        currency=None,
        bundle_offer=None,
        free_shipping=None,
        stock_urgency=None
    ):

        product_name = product_name.title()

        headlines = generate_headlines(
            product_name,
            price,
            discount_value,
            discount_percent,
            country
        )

        # ✅ chamada corrigida
        descriptions = generate_descriptions(
            product_name,
            price,
            discount_percent,
            guarantee_days,
            free_shipping,
            country
        )

        callouts = generate_callouts(country)

        keywords = generate_keywords(product_name, country)

        extra_transactional_headlines = []

        if bundle_offer:
            extra_transactional_headlines.append(bundle_offer.title())

        if stock_urgency:
            extra_transactional_headlines.append(stock_urgency.title())

        if free_shipping:
            extra_transactional_headlines.append(
                "Frete Grátis Hoje" if country == "BR" else "Free Shipping Today"
            )

        if guarantee_days:
            extra_transactional_headlines.append(
                f"{guarantee_days} Dias de Garantia"
                if country == "BR"
                else f"{guarantee_days} Day Guarantee"
            )

        if installments_text:
            extra_transactional_headlines.append(
                installments_text.replace(" ", "")
            )

        transactional_headlines = []

        # primeiro entram dados do produto
        for item in extra_transactional_headlines:
            if item:
                transactional_headlines.append(item)

        # depois entram headlines padrão
        for item in headlines["transactional"]:
            if item not in transactional_headlines:
                transactional_headlines.append(item)

        transactional_headlines = transactional_headlines[:15]

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
                    "headlines": transactional_headlines,
                    "descriptions": descriptions
                },
                "callouts": callouts
            }
        ]

        return campaigns