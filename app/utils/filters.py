def apply_filters(df, filters):

    for column, value in filters.items():

        if value is None:
            continue

        if column not in df.columns:
            continue

        col_series = df[column]

       
        if col_series.dtype == "object":

            df = df[
                col_series.astype(str)
                .str.strip()
                .str.lower() == str(value).strip().lower()]

        
        else:
            df = df[col_series == value]

    return df