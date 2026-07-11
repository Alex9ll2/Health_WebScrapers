import nodriver as uc
from asyncio import sleep
from random import uniform, randint

SCROLLING_STARTING_INTERVAL = 2
SCROLLING_ENDING_INTERVAL = 8
PAGINATION_STOP = 2
_UP = 0
_DOWN = 1
_MAIN_URL = "https://pubmed.ncbi.nlm.nih.gov/"

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

async def openingTabs(endpoints: list, browser: uc.Browser):
    for endpoint in endpoints:
        await sleep(uniform(2.5,3.6))
        tab = await browser.get(_MAIN_URL + endpoint, new_tab=True)
        await scrolling(tab)
        await sleep(uniform(2.5,3.6))
        await tab.close()

async def main(key: str):
    # Starting code
    search_bar_CSSselector = "#id_term"
    send_keys_CSSselector = "button.search-btn"
    result_CSSselector = "a.docsum-title"
    browser = await uc.start()
    searchPage = await browser.get(_MAIN_URL)

    # Security stop
    await sleep(uniform(1.5,3.4))

    # Send data
    await (await searchPage.find(search_bar_CSSselector, timeout=10)).send_keys(key)
    await (await searchPage.find(send_keys_CSSselector, timeout=10)).click()

    # Security stop
    await sleep(2.5,3.4)

    # Result information
    endpoints = None
    for _ in range(PAGINATION_STOP):
        await scrolling(searchPage)
        endpoints = await searchPage.find_all(result_CSSselector, timeout=10)
        endpoints = await formatingResults(endpoints)
    if endpoints is None:
        return
    await openingTabs(endpoints, browser)
    # Opening every endpoint in diferrent tabs


if __name__ == "__main__":
    uc.loop().run_until_complete(main("Blood cancer"))
    