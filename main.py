from playwright.sync_api import sync_playwright
from twilio.rest import Client
import time
from constants import *

client = Client(account_sid, auth_token)


def scrapeTitles():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://chia-anime.cc/")
        titles = page.locator("div.content_episode.recent_sub.datagrild div.name").all_text_contents()
        return titles


def observer(oldValue):
    newValue = scrapeTitles()
    if newValue != oldValue:
        difference = set(newValue) - set(oldValue)
        msg = "\n".join(difference)
        client.messages.create(
            from_=twilioNumber,
            to=myNumber,
            body="Mr.Nawaf Al-Jehani,\n" + "حلقات جديدة نزلت الان قد تهمك:\n" + msg
        )
        print("Content changed:\n" + msg)
        return newValue
    else:
        return oldValue


initialValue = scrapeTitles()
print("initialValue\n", scrapeTitles())

while True:
    time.sleep(60 * 60)
    initialValue = observer(initialValue)
