from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from cleantext import clean


def parse_text(text):
    text = text.replace("[", "expletive")
    parsed_text = clean(text, no_emoji=True,
                        no_punct=True,
                        no_line_breaks=True,
                        no_urls=True,
                        no_numbers=True,
                        no_emails=True,
                        strip_lines=True,
                        normalize_whitespace=True,
                        )
    return parsed_text


YOUTUBE_URL = "https://www.youtube.com/watch?v=kPH3Od-TUF0"
OUTPUT_CSV_FILE = './data/transcript.csv'

video_id = YOUTUBE_URL.split("v=")[1].strip()
transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)

if __name__ == "__main__":
    parsed_texts = []
    for segment in transcript_dict:
        text = segment["text"]
        parsed_text = parse_text(text)
        parsed_text = parsed_text.strip()
        parsed_texts.append(parsed_text)

    df_transcript = pd.DataFrame(parsed_texts)
    df_transcript.to_csv(OUTPUT_CSV_FILE, mode='a', index=True)
