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


url = "https://www.youtube.com/watch?v=kPH3Od-TUF0"
video_id = url.split("v=")[1].strip()
transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)

if __name__ == "__main__":
    for segment in transcript_dict:
        text = segment["text"]
        parsed_text = parse_text(text)
        parsed_text = parsed_text.strip()
        print(parsed_text)
