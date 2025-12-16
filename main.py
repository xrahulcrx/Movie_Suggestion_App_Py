import os
from recommender.recommend import load_movies, recommend_movies


# Get terminal size dynamically
try:
    # Gets the width of the line
    terminal_width = os.get_terminal_size().columns
except OSError:
    # if the terminal size cannot be determined
    terminal_width = 80

data_file = "data/movies.jl"

def main():
    project_title = "Movie Suggestion using Python"
    print('#' * terminal_width)
    print(project_title.center(terminal_width))
    print('#' * terminal_width)

    df = load_movies(data_file)
    if df is None:
        return

    genre = input("\nEnter genre (Drama, Action, Crime, etc.): ").strip()
    keyword = input("Enter keyword (optional – press Enter to skip): ").strip()

    result = recommend_movies(df, genre, keyword)

    print("\nRecommended Top 3 Movies:\n")

    if isinstance(result, str):
        print(result)
    else:
        for _, row in result.iterrows():
            print(f"""{row['title']} ({int(row['year'])})
            Rating: {row['rating']}
            Genre: {", ".join(row['genres'])}
            Plot:{row['plot']}""")

            print("-" * terminal_width)


if __name__ == "__main__":
    main()
