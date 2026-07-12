import nodriver as uc
from asyncio import sleep
from random import uniform, randint
import csv

SCROLLING_STARTING_INTERVAL = 2
SCROLLING_ENDING_INTERVAL = 8
PAGINATION_STOP = 10
_UP = 0
_DOWN = 1
_MAIN_URL = "https://pubmed.ncbi.nlm.nih.gov/"
FILE_NAME = "dumped_information.csv"

def writingHeaders():
    with open(FILE_NAME, mode='w', encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "DOI", "Title", "Authors", "Abstract"])

def writingInformation(data: list):
    """
    dataSet: Dictionary with information to be dumped

    This function may not work when working with parallel processing
    """

    with open(FILE_NAME, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

async def formatingResults(htmlLinks: list):
    endpoints = list()
    for link in htmlLinks:
        # Access al the tags from the <a></a>
        tags = link.attributes
        # [key1, value1, key2, value2]
        for index in range(0, len(tags), 2):
            if tags[index] == "href":
                endpoints.append(tags[index+1])

    return endpoints

async def scrolling(page: uc.Tab):
    scrollingTimes = randint(SCROLLING_STARTING_INTERVAL, SCROLLING_ENDING_INTERVAL)
    for _ in range(scrollingTimes):
        direction = randint(_UP,_DOWN)
        high_limit = randint(10,15)
        low_limit = randint(1,5)
        if direction == _DOWN:
            for pixel in range(low_limit, high_limit):
                await page.scroll_down(pixel)
        else:
            for pixel in range(low_limit, high_limit):
                await page.scroll_up(pixel)
        await sleep(1.2,2.1)

async def urlExtraction(page: uc.Tab):
    title_css_selector = "#full-view-heading .heading-title"
    authors_css_selector = "#full-view-heading .authors-list .full-name"
    doi_css_selector = "#full-view-heading .identifier.doi a.id-link"
    abstract_css_selector = "#eng-abstract p"
    url_css_selector = 'meta[property="og:url"]'
    try:
        doi = await page.find(doi_css_selector)
        doi = doi.text.replace("\n", "").strip()
    except Exception as e:
        return
    try:
        title = await page.find(title_css_selector)
        title = title.text.replace("\n", "").strip()
    except Exception as e:
        title = "No title available"
        print(e)
    try:
        authors = await page.find(authors_css_selector)
        authors = authors.text_all.replace("\n", "").strip().split(" ")
    except Exception as e:
        authors = "No authors available"
        print(e)

    try:
        abstract = await page.find(abstract_css_selector, timeout=3)
        abstract = abstract.text.replace("\n", "").strip()
    except Exception as e:
        abstract = "No abstract available"
        print(e)
    
    try:
        tab_url = await page.find(url_css_selector, timeout=3)
        url_attributes = tab_url.attributes
        page_url = None
        for index in range(len(url_attributes)):
            if url_attributes[index] == "content":
                page_url = url_attributes[index+1]
    except Exception as e:
        pass

    data = [page_url, doi, title, authors, abstract]
    writingInformation(data=data)
    
async def openingTabs(endpoints: list, browser: uc.Browser):

    for endpoint in endpoints:
        await sleep(uniform(2.5,3.6))
        tab = await browser.get(_MAIN_URL + endpoint, new_tab=True)

        await scrolling(tab)
        await sleep(uniform(2.5,3.6))
        # Extracting information
        await urlExtraction(tab)

        await tab.close()

async def startScraping(key: str):
    # Starting code
    search_bar_CSSselector = "#id_term"
    send_keys_CSSselector = "button.search-btn"
    result_CSSselector = "a.docsum-title"
    pagination_button_CSSselector = "button.next-page-btn"

    browser = await uc.start()
    searchPage = await browser.get(_MAIN_URL)
    await scrolling(searchPage)
    # Security stop
    await sleep(uniform(1.5,3.4))

    # Send data
    await (await searchPage.find(search_bar_CSSselector, timeout=10)).send_keys(key)
    await (await searchPage.find(send_keys_CSSselector, timeout=10)).click()

    # Security stop
    await sleep(2.5,3.4)

    # Opening every endpoint in diferent tabs
    writingHeaders()
    
    # Result information
    endpoints = None
    for _ in range(PAGINATION_STOP):
        await scrolling(searchPage)
        endpoints = await searchPage.find_all(result_CSSselector, timeout=10)
        endpoints = await formatingResults(endpoints)

        if endpoints is None:
            break
        await openingTabs(endpoints, browser)
        
        await (await searchPage.find(pagination_button_CSSselector)).click()
        await sleep(uniform(1.5,3.6))

def executeScraper(key: str):
    uc.loop().run_until_complete(startScraping(key))