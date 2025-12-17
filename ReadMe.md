# Python Project Submission - Rahul
## Movie Suggestion App using Py

### Project Description
The Movie Suggestion App is a Python code that recommends movies to users based on their preferred genre and keywords.
The project integrates web scraping, data processing, and recommendation logic using real-world movie data sourced from IMDb.

The application first scrapes movie data from the IMDb Top 250 Movies chart, processes and stores the data, and then provides movie suggestion using based on user input.

### Features

Scrapes movie data from IMDb using Scrapy and Selenium
Stores scraped data in a structured format (.jl)
Uses Pandas for data cleaning and filtering

#### Recommends Top 3 movies based on:
Genre
Keywords (IMDb keywords)

Falls back to genre-based suggestions if keywords are not found

### Concepts Used

Web Scraping (Scrapy, Selenium)
Data Processing (Pandas)
Error Handling
File Handling
Git & GitHub Version Control

### Python Libraries Used
scrapy
selenium
pandas
tqdm

### Project Structure
```
MovieSuggestionApp/
│
├── scrapper/
│   └── imdb_scrap.py
│
├── recommender/
│   └── recommend.py
│
├── data/
│   └── movies.jl
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```


## How to Run the Project

### Create & Activate Virtual Environment
```
python -m venv .venv
.venv\Scripts\activate
```

### Install Required Libraries
```
pip install -r requirements.txt
```

### Run the Scraper

-O ensures the file is overwritten each time instead of appending.
```
python -m scrapy runspider scrapper/imdb_scrap.py -O data/movies.jl
```


### Run the Movie Suggestion App
```
python main.py
```






