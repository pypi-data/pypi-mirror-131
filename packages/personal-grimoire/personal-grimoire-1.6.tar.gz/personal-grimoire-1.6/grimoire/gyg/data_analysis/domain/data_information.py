class Info:
    booking_table = "dwh.fact_booking"
    tour_table = "dwh.dim_tour"
    tour_option_table = "dwh.dim_tour_option"
    default_price_column = "adult_selling_price_eur"
    adp_event = "ActivityDetailPageRequest"
    raw_events_folder_old = "/mnt/analytics/raw/"
    raw_events_folder = "/mnt/quickline"
    cleaned_events_folder = "/mnt/analytics/cleaned/v1"
    reco_response = "RecoResponse"
    reco_impression = "RecommendationsImpression"
    reco_served = "RecommendationsServed"
    adpr = "ActivityDetailPageRequest"
    rnr_events = [
        adpr,
        reco_response,
        reco_impression,
        reco_served,
    ]
    datalake_names = {
        "tour_table": "dwh_dim_tour",
        "booking_table": "dwh_fact_booking",
        "tour_option_table": "dwh_dim_tour_option",
    }
    production_names = {
        "tour_table": "tour",
        "booking_table": "booking",
        "tour_option_table": "tour_option",
    }
