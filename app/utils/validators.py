VALID_REGIONS = {
    "dhaka": "Dhaka",
    "chittagong": "Chittagong",
    "sylhet": "Sylhet",
    "rajshahi": "Rajshahi",
    "khulna": "Khulna",
    "rangpur": "Rangpur",
    "barisal": "Barisal",
    "mymensingh": "Mymensingh"
}


VALID_FARM_TYPES = {
    "small": "Small",
    "medium": "Medium",
    "large": "Large",
    "commercial": "Commercial"
}


VALID_MARKET_TYPES = {
    "local": "Local",
    "wholesale": "Wholesale",
    "export": "Export",
    "retail": "Retail",
    "government procurement": "Government Procurement"
}


VALID_CROP_CATEGORIES = {
    "cereal": "Cereal",
    "vegetable": "Vegetable",
    "fruit": "Fruit",
    "pulse": "Pulse",
    "oilseed": "Oilseed",
    "cash crop": "Cash Crop",
    "spice": "Spice"
}

VALID_SEASONS = {
    "summer": "Summer",
    "winter": "Winter",
    "autumn": "Autumn",
    "spring": "Spring"
} 

VALID_GROWING_SEASONS = {
    "rabi": "Rabi",
    "kharif": "Kharif",
    "zaid": "Zaid",
    "year-round": "Year-Round"
}


VALID_YEARS = [2022, 2023, 2024]

VALID_QUALITY_GRADES = {
    "a": "A",
    "b": "B",
    "c": "C",
    "d": "D"
} 

VALID_QUARTERS = [1, 2, 3, 4] 

def validate_filter(
    value,
    valid_values,
    field_name
):

    if value is None:
        return None

    # STRING FILTERS
    if isinstance(value, str):

        normalized_value = value.strip().lower()

        if normalized_value not in valid_values:

            raise ValueError(
                f"Invalid {field_name}"
            )

        return valid_values[normalized_value]

    # INTEGER FILTERS
    else:

        if value not in valid_values:

            raise ValueError(
                f"Invalid {field_name}"
            )

        return value 