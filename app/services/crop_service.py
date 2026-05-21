from app.utils.data_loaders import load_harvest_data, load_crop_revenue, load_crop_dimension

from app.utils.filters import apply_filters
from app.utils.constants import water_requirement_map, benchmark_yield

import pandas as pd


def get_yield_efficiency(
    df: pd.DataFrame,
    crop_category=None,
    season=None,
    year=None,
    region=None,
    water_requirement=None):

    filters = {"crop_category": crop_category,"season": season,"year": year,"region": region}

    # reusable centralized filtering
    df = apply_filters(df, filters)

    grouped = df.groupby(["crop_name", "crop_category", "season"], as_index=False).agg(total_area_planted_ha=("area_planted_ha", "sum"),total_yield=("quantity_harvested_ton", "sum"))

    grouped["actual_avg_yield_ton_per_ha"] = (grouped["total_yield"] / grouped["total_area_planted_ha"]).round(1)

    grouped["avg_yield_benchmark_ton_per_ha"] = (grouped["crop_name"].map(benchmark_yield))

    grouped["efficiency_pct"] = (grouped["actual_avg_yield_ton_per_ha"] / grouped["avg_yield_benchmark_ton_per_ha"]) * 100

    grouped["efficiency_pct"] = (grouped["efficiency_pct"].round(1))

    grouped["water_requirement"] = (grouped["crop_name"].map(water_requirement_map))

    # water requirement filter
    if water_requirement is not None:

        grouped = grouped[grouped["water_requirement"].astype(str).str.lower() == water_requirement.strip().lower()]

    return grouped 


def get_crop_trend(df: pd.DataFrame,
    crop_name=None,
    crop_category=None,
    year=None,
    quarter=None,
    market_type=None):

    filters = {"crop_name": crop_name,
        "crop_category": crop_category,
        "year": year,
        "quarter": quarter,
        "market_type": market_type}


    df = apply_filters(df, filters)

    grouped = (
        df.groupby(
            ["crop_name", "year", "quarter", "season"],as_index=False)
        .agg(total_quantity_sold_ton=("quantity_harvested_ton","sum"),

            total_revenue_bdt=("revenue_bdt","sum"),

            avg_price_per_ton_bdt=("price_per_ton_bdt","mean"),

            num_harvests=("harvest_id","count")))

    grouped["total_quantity_sold_ton"] = (grouped["total_quantity_sold_ton"].round(1))

    grouped["total_revenue_bdt"] = (grouped["total_revenue_bdt"].round(1))

    grouped["avg_price_per_ton_bdt"] = (grouped["avg_price_per_ton_bdt"].round(1))

    return grouped



def get_quality_breakdown(
    crop_id=None,
    crop_category=None,
    year=None,
    region=None,
    market_type=None,
    pesticide_residue=None):

    df = load_harvest_data()

    # crop_id -> crop_name mapping
    if crop_id is not None:

        crop_df = load_crop_dimension()

        crop_match = crop_df[crop_df["crop_id"] == crop_id]

        if crop_match.empty:

            df = df.iloc[0:0]

        else:

            crop_name = (
                crop_match.iloc[0]["crop_name"]
            )

            df = df[
                df["crop_name"] == crop_name
            ]


    # remaining filters
    filters = {"crop_category": crop_category,
        "year": year,
        "region": region,
        "market_type": market_type,
        "pesticide_residue": pesticide_residue}

    df = apply_filters(df, filters)

    total_records = len(df)


    # Grade Distribution
    grade_distribution = {}

    grades = ["A", "B", "C", "D"]

    for grade in grades:

        grade_df = df[df["quality_grade"] == grade]

        count = len(grade_df)

        pct = ((count / total_records) * 100
            if total_records > 0 
            else 0)

        avg_revenue = (
            grade_df["revenue_bdt"].mean()
            if count > 0 
            else 0)

        grade_distribution[grade] = {
            "count": count,
            "pct": round(pct, 1),
            "avg_revenue_bdt": round(avg_revenue, 1)}


    # Pesticide Breakdown
    pesticide_breakdown = {}

    residue_levels = [
        "None",
        "Trace",
        "Low",
        "High"]

    for residue in residue_levels:

        residue_df = df[df["pesticide_residue"] == residue]

        count = len(residue_df)

        pct = ((count / total_records) * 100
            if total_records > 0 
            else 0)

        pesticide_breakdown[residue] = {
            "count": count,
            "pct": round(pct, 1)}

    return {
        "total_records": total_records,
        "grade_distribution": grade_distribution,
        "pesticide_residue_breakdown": pesticide_breakdown} 
