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


VALID_PRICE_TIERS = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "premium": "Premium"
}


VALID_DISTRICTS = {
    "gazipur": "Gazipur",
    "comilla": "Comilla",
    "narsingdi": "Narsingdi",
    "mymensingh": "Mymensingh",
    "tangail": "Tangail",
    "sylhet": "Sylhet",
    "rangamati": "Rangamati",
    "chapainawabganj": "Chapainawabganj",
    "rangpur": "Rangpur",
    "manikganj": "Manikganj",
    "sirajganj": "Sirajganj",
    "jamalpur": "Jamalpur",
    "noakhali": "Noakhali",
    "feni": "Feni",
    "kurigram": "Kurigram",
    "kishoreganj": "Kishoreganj",
    "gopalganj": "Gopalganj",
    "jashore": "Jashore",
    "rajshahi": "Rajshahi",
    "sunamganj": "Sunamganj",
    "moulvibazar": "Moulvibazar",
    "lalmonirhat": "Lalmonirhat",
    "satkhira": "Satkhira",
    "bhola": "Bhola",
    "patuakhali": "Patuakhali",
    "barisal": "Barisal",
    "pabna" : "Pabna",
    "cox's bazar" : "Cox's Bazar"
} 


VALID_PESTICIDE_RESIDUES = {
    "none": "None",
    "trace": "Trace",
    "low": "Low",
    "high": "High"
} 


VALID_CROP_IDS = [1, 2, 3, 4, 5]

def validate_filter(
    value,
    valid_values,
    field_name
):

    if value is None:
        return None


    if isinstance(value, str):

        normalized_value = value.strip().lower()

        if normalized_value not in valid_values:

            allowed_values = list(valid_values.values()) 

            raise ValueError(
                f"Invalid {field_name}. "
                f"Allowed values: "
                f"{', '.join(map(str, allowed_values))}")

        return valid_values[normalized_value]

  
    else:

        if value not in valid_values:

            raise ValueError(
                f"Invalid {field_name}. "
                f"Allowed values: "
                f"{', '.join(map(str, valid_values))}")

        return value 