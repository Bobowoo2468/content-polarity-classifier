import time

import selenium.common.exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import pandas as pd
from cleantext import clean
import regex as re

# enable the headless mode
options = Options()
options.add_argument("--headless=new")


def scrape(youtube_video_url):
    comments = []
    driver = Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    driver.get(youtube_video_url)
    driver.maximize_window()

    # wait for YouTube to load the page comments
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata'))
        )

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='more-replies']"))
        )
        more_replies = driver.find_elements(By.XPATH, "//*[@id='more-replies']")
        # print(len(more_replies))

        for more_reply in more_replies:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(more_reply)).click()

    except selenium.common.exceptions.TimeoutException:
        print("No element to render")

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since Youtube dynamically loads them).
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down until "next load"
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            # print("No more comments required to render!")
            break
        last_height = new_height

    try:
        # Extract the element that refers to the comments
        comment_section = driver.find_elements(By.XPATH, '//*[@id="comments"]')

    except exceptions.NoSuchElementException:
        # in case Youtube changes their HTML layouts
        error = "Element not found: HTML layout changed"
        print(error)

    try:
        is_looped = False

        while True:
            # Extract the elements storing the usernames and comments
            # username_html_elements = driver.find_elements(By.XPATH, '//*[@id="author-text"]')
            comment_html_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

            for comment_index, comment_element in enumerate(comment_html_elements):
                if comment_index == 0 and is_looped:
                    return comments

                if comment_index == 0:
                    is_looped = True

                comment_text = comment_element.text
                words = comment_text.split()
                removed_tag_words = [word for word in words if not word.startswith("@")]
                removed_tag_comment = ' '.join(removed_tag_words)
                parsed_comment = parse_comment(removed_tag_comment)
                parsed_comment = parsed_comment.strip()

                if len(parsed_comment) != 0:
                    comments.append(parsed_comment)
                else:
                    print("Empty comment, not added into scraped comments!")

    except exceptions.NoSuchElementException:
        # in case Youtube changes their HTML layouts
        error = "Element not found: HTML layout changed"
        print(error)


def reinitialise():
    return [], [], 0


def parse_comment(comment):
    parsed_comment = clean(comment, no_emoji=True,
                           no_punct=True,
                           no_line_breaks=True,
                           no_urls=True,
                           no_numbers=True,
                           no_emails=True,
                           strip_lines=True,
                           normalize_whitespace=True,
                           )
    return parsed_comment


if __name__ == "__main__":
    YOUTUBE_URL = "https://www.youtube.com/watch?v=kPH3Od-TUF0"
    OUTPUT_CSV_FILE = './data/comments.csv'

    comments = scrape(YOUTUBE_URL)
    print("Number of comments: ", len(comments))

    df_comments = pd.DataFrame(comments)
    df_comments.to_csv(OUTPUT_CSV_FILE, mode='a', index=True)
