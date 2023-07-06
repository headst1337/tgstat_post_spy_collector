import datetime
import re
import time
import requests
import random
from urllib.parse import urlencode
from apscheduler.schedulers.background import BackgroundScheduler

from run import app
from app import db
from app.models.post import Post
from app.config import Config


def extract_filtered_data(text: str) -> str|None:
    card_pattern = r'\d{12,19}'
    crypto_pattern = r'(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z0-9]{26,35})'
    mono_pattern = r'https://send\.monobank\.ua/jar/[a-zA-Z0-9]+'
    patterns = [card_pattern, crypto_pattern, mono_pattern]
    result_data = ' '.join([match for pattern in patterns for match in re.findall(pattern, text)])
    result_data = ' '.join(list(dict.fromkeys(result_data.split())))
    return result_data if len(result_data) > 0 else None

def fetch_from_api(session, offset) -> None:
    #end_date = int(time.time())
    #start_date = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp())
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
        # 'startDate': start_date,
        # 'endDate': end_date,
        'extendedSyntax': 1
    }

    url = base_url + '?' + urlencode(query_params)
    response = session.get(url)
    data = response.json()
    for item in data['response']['items']:
        post_link = item['link']
        group_link = next((channel['link'] for channel in data['response']['channels'] if channel['id'] == item['channel_id']), None)
        body = item['text']
        payment_data = extract_filtered_data(item['text'])
        if payment_data:
            timestamp = item['date']
            post = Post(post_link=post_link, group_link=group_link, body=body, payment_data=payment_data, timestamp=datetime.datetime.fromtimestamp(timestamp))
            save_object(post)
        else: print("No payment data")

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
        for _ in range(100):
            random_offset = random.randint(0, 1000)
            while random_offset in unique_offset:
                random_offset = random.randint(0, 1000)
                unique_offset.add(random_offset)
            print(f"Offset: {random_offset}")
            fetch_from_api(session, random_offset)


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_data, trigger="interval", days=3)