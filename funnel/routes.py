@router.get("/keywords/{keyword_id}")
def get_keyword_funnel(keyword_id: int, db: Session = Depends(get_db)):

    data = build_keyword_funnel(keyword_id, db)

    if not data:
        return {
            "keyword_id": keyword_id,
            "impressions": 0,
            "clicks": 0,
            "visitors": 0,
            "checkouts": 0,
            "conversions": 0,
            "upsells": 0,
            "message": "No data yet"
        }

    return data