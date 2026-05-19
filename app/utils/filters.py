def apply_filters(df, filters):

    for column, value in filters.items():

        if value is None:
            continue

        if column not in df.columns:
            continue

        df = df[df[column] == value]

    return df 