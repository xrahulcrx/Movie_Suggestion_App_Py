import scrapy
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from tqdm import tqdm


class SpiderIMDB(scrapy.Spider):
    name = "imdb_bot"

    custom_settings = {
        "LOG_LEVEL": "ERROR",
        "ROBOTSTXT_OBEY": False,
        "FEED_EXPORT_ENCODING": "utf-8",

        # settings for multiple requests
        "CONCURRENT_REQUESTS": 32,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 16,
        "DOWNLOAD_DELAY": 0.2,
        "RANDOMIZE_DOWNLOAD_DELAY": True,

        # Timeouts
        "DOWNLOAD_TIMEOUT": 20,

        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    total_movies = 250


    # STEP 1: Top 250 movie charts with Title and link
    def start_requests(self):

        #initialize selenium and not running in headless since imdb blocks bots
        #trigger the browser, runs & load the webpage once to get the movie titles and links

        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")

        print("Triggering Selenium using browser")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.imdb.com/chart/top/")
        time.sleep(5)

        #once loaded - gets the view source page
        html = driver.page_source
        #closing the selenium
        driver.quit()

        #parse the source page to scrapy
        response = Selector(text=html)
        movies = response.css("li.ipc-metadata-list-summary-item")

        self.pbar = tqdm(
            total=self.total_movies,
            desc="Scraping movies",
            unit="movie"
        )

        #iterations for each movie titles and links
        for movie in movies:
            title = movie.css("h3.ipc-title__text::text").get()

            link = movie.css(
                "a.ipc-title-link-wrapper::attr(href)"
            ).get()

            if not link:
                continue

            #since only partial link in webpage, adding domain link as combined link
            link = "https://www.imdb.com" + link.split("?")[0]

            yield scrapy.Request(
                url=link,
                callback=self.parse_movie,
                meta={
                    "title": title,
                    "url": link
                }
            )

    # STEP 2: Parsing each movie link and getting data from json-ld
    def parse_movie(self, response):

        #gets the json file from movie link
        json_ld = response.css(
            'script[type="application/ld+json"]::text'
        ).get()

        #required data to fetch from json
        genres = []
        plot = None
        rating = None
        votes = None
        year = None
        duration = None
        keyword = None
        keywords = None

        #check if json available or not
        if json_ld:
            try:
                #loading the json data
                data = json.loads(json_ld)

                #fetching the genre and plot using the tags
                genres = data.get("genre", [])
                plot = data.get("description")

                # get ratings and votes
                aggregate = data.get("aggregateRating", {})
                rating = aggregate.get("ratingValue")
                votes = aggregate.get("ratingCount")

                # get only year from json file
                date_pub = data.get("datePublished")
                year = date_pub[:4] if date_pub else "NA"

                meta_duration = data.get("duration")
                h = re.search(r"(\d+)H", meta_duration or "")
                m = re.search(r"(\d+)M", meta_duration or "")
                duration = (
                    f"{h.group(1)}h {m.group(1)}m"
                    if h and m
                    else None
                )

                keyword = data.get("keywords")
                keywords = [k.strip() for k in keyword.split(",")] if keyword else []



            except json.JSONDecodeError:
                pass

        self.pbar.update(1)

        yield {
            "title": response.meta["title"] or "NA",
            "year": year or "NA",
            "rating": rating or "NA",
            "votes": votes or "NA",
            "duration": duration or "NA",
            "url": response.meta["url"],

            "plot": plot or "NA",
            "genres": genres or [],
            "keywords" : keywords or []
        }

    def closed(self, reason):
        if hasattr(self, "pbar"):
            self.pbar.close()

