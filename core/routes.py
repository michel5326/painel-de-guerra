@router.get("/products/{product_id}/dashboard")
def product_dashboard(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {"message": "Product not found"}

    all_keywords = []
    total_cost = 0
    total_revenue = 0
    total_conversions = 0

    for campaign in product.campaigns or []:
        for keyword in campaign.keywords or []:

            logs = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            ).all()

            if not logs:
                continue

            cost = sum(log.cost for log in logs)
            revenue = sum(log.revenue for log in logs)
            conversions = sum(log.conversions for log in logs)

            total_cost += cost
            total_revenue += revenue
            total_conversions += conversions

            roas = revenue / cost if cost > 0 else 0

            if roas >= product.min_roas:
                status = "🟢"
            else:
                status = "🟡"

            all_keywords.append({
                "keyword": keyword.keyword,
                "roas": round(roas, 2),
                "conversions": conversions,
                "cost": round(cost, 2),
                "revenue": round(revenue, 2),
                "status": status
            })

    roas_total = total_revenue / total_cost if total_cost > 0 else 0
    cpa_medio = total_cost / total_conversions if total_conversions > 0 else 0

    if roas_total >= product.min_roas:
        product_status = "🟢 Saudável"
    else:
        product_status = "🟡 Sob pressão"

    return {
        "product": product.name,
        "receita_total": round(total_revenue, 2),
        "custo_total": round(total_cost, 2),
        "roas_medio": round(roas_total, 2),
        "cpa_medio": round(cpa_medio, 2),
        "status_geral": product_status,
        "keywords": all_keywords
    }