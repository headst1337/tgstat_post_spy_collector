import asyncio
import datetime
import re
import time
import aiohttp
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from run import app
from app import db
from app.models.post import Post
from app.config import Config


async def extract_filtered_data(text: str) -> str|None:
    card_pattern = r'\d{12,19}'
    crypto_pattern = r'(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z0-9]{26,35})'
    mono_pattern = r'https://send\.monobank\.ua/jar/[a-zA-Z0-9]+'
    patterns = [card_pattern, crypto_pattern, mono_pattern]
    result_data = ' '.join([match for pattern in patterns for match in re.findall(pattern, text)])
    return result_data if len(result_data) > 0 else None

async def fetch_from_api(session, offset, limit):
    end_date = int(time.time())
    start_date = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp())
    base_url = 'https://api.tgstat.ru/posts/search'
    query_params = {
        'token': Config.TGSTAT_TOKEN,
        'q': Config.KEYWORDS,
        'extended': 1,
        'offset': offset,
        'limit': limit,
        'country': 'ua',
        'language': 'ukrainian',
        'hideForwards': 1,
        'startDate': start_date,
        'endDate': end_date,
        'extendedSyntax': 1
    }

    url = base_url + '?' + urlencode(query_params)
    async with session.get(url) as response:
        data = await response.json()
        posts = []
        for item in data['response']['items']:
            post_link = item['link']
            group_link = next((channel['link'] for channel in data['response']['channels'] if channel['id'] == item['channel_id']), None)
            body = item['text']
            payment_data = await extract_filtered_data(item['text'])
            if payment_data:
                timestamp = item['date']
                post = Post(post_link=post_link, group_link=group_link, body=body, payment_data=payment_data, timestamp=datetime.datetime.fromtimestamp(timestamp))
                posts.append(post)
            with ThreadPoolExecutor() as executor:
                await asyncio.get_running_loop().run_in_executor(executor, save_objects, posts)

def save_objects(posts):
    with app.app_context():
        with db.session() as session:
            filtered_posts = []
            for post in posts:
                payment_data_words = post.payment_data.split(' ')
                existing_post = session.query(Post).filter((Post.body == post.body) | (Post.payment_data.in_(payment_data_words))).first()
                if existing_post is None:
                    filtered_posts.append(post)
            if filtered_posts:
                session.bulk_save_objects(filtered_posts)
                session.commit()

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        with ThreadPoolExecutor() as executor:
            tasks = []
            limit = 50
            loop = asyncio.get_event_loop()
            for offset in range(0, 100):
                task = await loop.run_in_executor(executor, fetch_from_api, session, offset, limit)
                tasks.append(task)
            await asyncio.gather(*tasks)

scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: asyncio.run(fetch_data()), trigger="interval", days=3)
