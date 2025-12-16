import pandas as pd


def load_movies(filepath):
    try:
        df = pd.read_json(filepath, lines=True)

        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

        # Fix plot
        df["plot"] = df["plot"].fillna("")

        # ensure genres is always a list
        df["genres"] = df["genres"].apply(
            lambda x: x if isinstance(x, list) else []
        )

        df["keywords"] = df["keywords"].apply(
            lambda x: " ".join(x).lower() if isinstance(x, list) else ""
        )

        return df

    except Exception as e:
        print("Error loading movie data:", e)
        return None


def recommend_movies(df, genre, keyword, top_n=3):
    genre = genre.lower().strip()
    keyword = keyword.lower().strip()

    # filter by genre
    genre_filtered = df[
        df["genres"].apply(
            lambda g: genre in [x.lower() for x in g]
        )
    ]

    if genre_filtered.empty:
        return "No movies found for the given genre."

    # filter by genre and keywords
    if keyword:
        keyword_filtered = genre_filtered[
            genre_filtered["keywords"].str.contains(keyword, na=False)
        ]

        # combined filter
        if not keyword_filtered.empty:
            result = keyword_filtered
        else:
            # no keyword gets only genre
            print(f"No movies found {genre} and {keyword}, suggestion based on {genre}.")
            result = genre_filtered
    else:
        # default only genre
        result = genre_filtered

    # ratings
    result = result.sort_values(by="rating", ascending=False)

    # output
    return result[[
        "title",
        "plot",
        "rating",
        "year",
        "genres"
    ]].head(top_n)
