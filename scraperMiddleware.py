from healthScraper import executeScraper
from EmptyStringException import EmptyStringError

def scraperMiddleware(key: str):
    if not key:
        raise EmptyStringError
    else:
        executeScraper(key)