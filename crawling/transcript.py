from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import json

def extract_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    else:
        return None

def transcript(video_id):
    transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])

    full_text = " ".join([entry['text'] for entry in transcripts])
    with open('./translate/summary.json', 'w', encoding='utf-8') as json_file:
        json.dump(full_text, json_file, ensure_ascii=False, indent=4)

    return full_text

def sumy(full_text):
    parser = PlaintextParser.from_string(full_text, Tokenizer("en"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)

    return_values = []

    for sentence in summary:
        return_values.append(sentence.text)


    return True

video_id = extract_video_id("https://www.youtube.com/watch?v=dKKRwe8DPw8")
# print(video_id)
tt = transcript(video_id)
print(tt)
# print(tt)
# values = sumy(tt)

# print(values)