import os
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# enable the headless mode
options = Options()


# options.add_argument("--headless=new")


def get_video_transcript(url: str, video_id: int, transcripts_dict):
    """
        return the video transcripts as DataFrames
        :return : chapters_df, transcripts_df
        if not exist return None, None
    """

    driver = Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    driver.maximize_window()

    is_not_expanded = True

    while is_not_expanded:
        try:
            show_more_button = wait.until(
                EC.element_to_be_clickable(driver.find_element(By.ID, 'description-inline-expander')))
            show_more_button.click()
        except NoSuchElementException:
            print("Not rendered yet!")
        else:
            is_not_expanded = False
            print("Finally")
    try:
        transcript_button = wait.until(EC.element_to_be_clickable(
            driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Show transcript')]")))
        transcript_button.click()
    except NoSuchElementException:
        print("No transcript exists!")

    video_txt = ""
    try:
        transcripts = driver.find_elements(By.XPATH, "//yt-formatted-string[contains(@class,'segment-text')]")

    except NoSuchElementException:
        print("No such element exists!")
        return None

    for transcript in transcripts:
        print(transcript.text)
    # if 'header' in transcript.tag_name:
    #     curr_cid = len(chapters_dict['headline'])
    #     chapters_dict['headline'].append(transcript.text)
    #     chapters_dict['txt'].append("")
    #     chapters_dict['vid'].append(video_id)
    # else:
    #     data = transcript.text.splitlines()  # [timestamp, txt]
    #     video_txt += " " + data[1]
    #     transcripts_dict['cid'].append(curr_cid)
    #     transcripts_dict['timestamp'].append(data[0])
    #     transcripts_dict['txt'].append(data[1])
    #     transcripts_dict['vid'].append(video_id)
    # if curr_cid != -1:
    #     chapters_dict['txt'][curr_cid] += " " + data[1]

    return video_txt


if __name__ == '__main__':
    # chapters_dict = {
    #     'headline': [],
    #     'txt': [],
    #     'vid': [],
    # }

    transcripts_dict = {
        'txt': [],
        'timestamp': [],
        'cid': [],
        'vid': []
    }

    txt = get_video_transcript(
        "https://www.youtube.com/watch?v=kPH3Od-TUF0",
        0,
        transcripts_dict
    )
    print(txt)
