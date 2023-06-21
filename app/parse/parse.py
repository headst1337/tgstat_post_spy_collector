"""
Парсинг работает следующим образом:
В цикле for от 0 до 1000 (возможно ассинхронно)
делать запос на api tgstat и получать данные (со смещением offset).
После получения нужно распасить данные, а также
распарсить по регулярке платеные данные.
И записать в бд.
"""

import asyncio
import datetime
import re
import time
import aiohttp
from urllib.parse import urlencode
from ..models.post import Post
from .. import db
from apscheduler.schedulers.background import BackgroundScheduler
from ..config import Config

def extract_payment_data(text: str) -> str:
    pattern = r'\b\d{16}\b'
    matches = re.findall(pattern, text)
    return matches[0]

async def fetch_from_api(session, offset, limit):
    end_date = int(time.time())  # Текущая дата в формате timestamp
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
        'endDate': end_date
    }

    url = base_url + '?' + urlencode(query_params)
    async with session.get(url) as response:
        data = await response.json()
        for item in data['response']['items']:
            entry = Post(
                post_link=item['link'],
                group_link=next((channel['link'] for channel in data['response']['channels'] if channel['id'] == item['channel_id']), None),
                body=item['text'],
                payment_data=extract_payment_data(item['text']),
                timestamp=item['date']
            )
            db.session.add(entry)
        db.session.commit()

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        limit = 50
        for offset in range(0, 101, limit):
            task = asyncio.ensure_future(fetch_from_api(session, offset, limit))
            tasks.append(task)
        await asyncio.gather(*tasks)

scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: asyncio.run(fetch_data()), trigger="interval", days=3)
scheduler.start()
