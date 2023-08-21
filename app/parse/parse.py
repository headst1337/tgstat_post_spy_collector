import datetime
import re
import requests
import random

from run import app
from app import db
from app.models.post import Post
from app.config import Config

from urllib.parse import urlencode


def extract_filtered_data(text: str) -> str|None:

    crypto_pattern = r'(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z0-9]{26,35})'
    mono_link_pattern = r'https://send\.monobank\.ua/jar/[a-zA-Z0-9]+'
    card_pattern = r'(\d{4}\s?\d{4}\s?\d{4}\s?\d{4})|(\d{16})'

    patterns = [crypto_pattern, mono_link_pattern, card_pattern]

    result_data = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    result_data.extend(match)
                else:
                    result_data.append(match)

    return '\n'.join(list(dict.fromkeys(result_data))) if result_data else None

def fetch_from_api(session, offset) -> None:
    base_url = 'https://api.tgstat.ru/posts/search'
    query_params = {
        'token': Config.TGSTAT_TOKEN,
        'q': Config.KEYWORDS,
        'extended': 1,
        'offset': offset,
        'limit': 50,
        'country': 'ua',
        'language': 'ukrainian',
        'hideForwards': 1,
        'extendedSyntax': 1
    }

    url = base_url + '?' + urlencode(query_params)
    response = session.get(url)
    data = response.json()
    if 'response' in data and 'items' in data['response']:
        for item in data['response']['items']:
            post_link = item['link']
            group_link = next((channel['link'] for channel in data['response']['channels'] if channel['id'] == item['channel_id']), None)
            body = item['text']
            payment_data = extract_filtered_data(item['text'])
            if payment_data:
                timestamp = item['date']
                post = Post(post_link=post_link, group_link=group_link, body=body, payment_data=payment_data, timestamp=datetime.datetime.fromtimestamp(timestamp))
                save_object(post)
            else:
                print("No payment data")
    else:
        print("No 'items' in 'response' data")

def save_object(post) -> None:
    with app.app_context():
        with db.session() as session:
            existing_post = session.query(Post).filter((Post.body == post.body) | (Post.payment_data == post.payment_data)).first()
            if existing_post is None:
                session.add(post)
                session.commit()
                print("Post saved!")
            else:
                print("Post exists")

def fetch_data() -> None:
    with requests.Session() as session:
        unique_offset = set()
        for i in range(100):
            random_offset = random.randint(0, 1000)
            while random_offset in unique_offset:
                random_offset = random.randint(0, 1000)
                unique_offset.add(random_offset)
            print(f"Iter: {i} | Offset: {random_offset}")
            fetch_from_api(session, random_offset)
