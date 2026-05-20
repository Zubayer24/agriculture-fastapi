from app.utils.data_loaders import (
    load_harvest_data,
    load_farm_profitability,
    load_farm_by_id
) 

from app.utils.filters import apply_filters


def get_farm_summary(
    region=None,
    farm_type=None,
    year=None,
    season=None
):

    df = load_harvest_data()

    filters = {
        "region": region,
        "farm_type": farm_type,
        "year": year,
        "season": season
    }

    df = apply_filters(df, filters)

    grouped_df = (
        df.groupby(
            ["farm_name", "region", "farm_type"],
            as_index=False
        )
        .agg(
            total_revenue_bdt=("revenue_bdt", "sum"),
            total_cost_bdt=("input_cost_bdt", "sum"),
            net_profit_bdt=("net_profit_bdt", "sum"),
            avg_loss_pct=("loss_pct", "mean")
        )
    )

    return grouped_df


def get_farm_performance(
    farm_id,
    year=None,
    crop_category=None,
    market_type=None
):

    farm_df = load_farm_by_id(farm_id)

    if farm_df.empty:
        return None, None
    
    farm_name = farm_df.iloc[0]["farm_name"]

    df = load_harvest_data()

    filters = {
        "farm_name": farm_name,
        "year": year,
        "crop_category": crop_category,
        "market_type": market_type
    }

    df = apply_filters(df, filters)

    performance_df = (
        df.groupby(
            ["crop_name", "year", "market_type","quality_grade"],
            as_index=False
        )
        .agg(
            quantity_sold_ton=("quantity_sold_ton", "sum"),
            revenue_bdt=("revenue_bdt", "sum"),
            net_profit_bdt=("net_profit_bdt", "sum")
        )
    )

    return farm_df, performance_df


def get_top_farms(
    metric="profit",
    region=None,
    farm_type=None,
    year=None,
    limit=10
):

    df = load_farm_profitability()

    filters = {
        "region": region,
        "farm_type": farm_type,
        "year": year
    }

    df = apply_filters(df, filters)

    if metric == "profit":
        df["ranking_value"] = df["total_profit_bdt"]

    elif metric == "revenue":
        df["ranking_value"] = df["total_revenue_bdt"]

    elif metric == "yield":
        df["ranking_value"] = df["total_profit_bdt"] / df["total_cost_bdt"]

    else:
        raise ValueError("metric must be profit | revenue | yield")

    df = df.sort_values(
        by="ranking_value",
        ascending=False
    )

    df = df.head(limit).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df 



def get_loss_analysis(
    region=None,
    year=None,
    season=None,
    growing_season=None,
    quality_grade=None,
    crop_category=None
): 

    df = load_harvest_data()

    filters = {
        "region": region,
        "year": year,
        "season": season,
        "growing_season": growing_season,
        "quality_grade": quality_grade,
        "crop_category": crop_category
    }

    df = apply_filters(df, filters)

    # Summary 
    total_harvested = df["quantity_harvested_ton"].sum()

    total_lost = df["quantity_lost_ton"].sum()

    overall_loss_pct = (
        (total_lost / total_harvested) * 100
        if total_harvested > 0 else 0
    )  

    summary = {
        "total_harvested_ton": round(total_harvested, 1),
        "total_lost_ton": round(total_lost, 1),
        "overall_loss_pct": round(overall_loss_pct, 1)
    } 

    # breakdown 
    breakdown_df = (
        df.groupby(
            ["region", "crop_category", "quality_grade", "pesticide_residue"],
            as_index=False
        ) 
        .agg(
            total_lost_ton=("quantity_lost_ton", "sum"),
             total_harvested_ton=("quantity_harvested_ton", "sum")
        )
    )

    breakdown_df["loss_pct"] = (
        breakdown_df["total_lost_ton"]
        / breakdown_df["total_harvested_ton"]) * 100 

    breakdown_df["loss_pct"] = (
        breakdown_df["loss_pct"].round(1)
    )

    return summary, breakdown_df  