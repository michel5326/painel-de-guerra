@router.get("/")
def list_prospects(db: Session = Depends(get_db)):

    prospects = db.query(models.Prospect).all()

    result = []

    for p in prospects:

        average_bid = (p.top_bid_low + p.top_bid_high) / 2 if p.top_bid_low and p.top_bid_high else 0
        cost_20_clicks = average_bid * 20
        viability_ratio = p.commission_value / cost_20_clicks if cost_20_clicks > 0 else 0

        if viability_ratio > 1:
            viability_status = "🟢 Promissor"
        elif viability_ratio > 0.7:
            viability_status = "🟡 Arriscado"
        else:
            viability_status = "🔴 Inviável"

        result.append({
            "id": p.id,
            "product_name": p.product_name,
            "platform": p.platform,
            "country": p.country,
            "search_volume_last_month": p.search_volume_last_month,
            "commission_value": p.commission_value,
            "top_bid_low": p.top_bid_low,
            "top_bid_high": p.top_bid_high,
            "average_bid": round(average_bid, 2),
            "cost_20_clicks": round(cost_20_clicks, 2),
            "viability_ratio": round(viability_ratio, 2),
            "viability_status": viability_status,
            "temperature_ranking": p.temperature_ranking,
            "observations": p.observations
        })

    return result