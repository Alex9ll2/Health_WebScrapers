import nodriver as uc
from asyncio import sleep
from random import uniform, randint

SCROLLING_STARTING_INTERVAL = 2
SCROLLING_ENDING_INTERVAL = 8
_UP = 0
_DOWN = 1

async def formatingResults():
    cleanedLinks = list()

async def scrolling(page: uc.Tab):
    scrollingTimes = randint(SCROLLING_STARTING_INTERVAL, SCROLLING_ENDING_INTERVAL)
    for _ in scrollingTimes:
        direction = randint(_UP,_DOWN)
        high_limit = randint(10,15)
        low_limit = randint(1,5)
        if direction == _DOWN:
            for pixel in range(low_limit, high_limit):
                page.scroll_down(pixel)
        else:
            for pixel in range(low_limit, high_limit):
                page.scroll_up(pixel)
        await sleep(1.2,2.1)


async def main(key: str):
    search_bar_CSSselector = "#id_term"
    send_keys_CSSselector = "button.search-btn"
    browser = await uc.start()
    searchPage = await browser.get("https://pubmed.ncbi.nlm.nih.gov/")
    await sleep(uniform(1.5,3.4))
    await (await searchPage.find(search_bar_CSSselector)).send_keys(key)
    await (await searchPage.find(send_keys_CSSselector)).click()
    await sleep(2.5,3.4)
    searchResults = await searchPage.find_all("article.full-docsum", timeout=5)




if __name__ == "__main__":
    uc.loop().run_until_complete(main("Lung cancer"))
    