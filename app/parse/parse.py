"""
Парсинг работает следующим образом:
В цикле for от 0 до 1000 (возможно ассинхронно)
делать запос на api tgstat и получать данные (со смещением offset).
После получения нужно распасить данные, а также
распарсить по регулярке платеные данные.
И записать в бд.
"""




# import requests
# from ..models.post import Post
# from .. import db
# from apscheduler.schedulers.background import BackgroundScheduler


# def fetch_from_api():
#     response = requests.get('http://api.com/data')
#     data = response.json()
#     for item in data:
#         entry = Post(
#             body=item['body']
#             ...
#             )
#         db.session.add(entry)
#     db.session.commit()


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=fetch_from_api, trigger="interval", days=3)
# scheduler.start()
