from notion_planner import return_planner_img, yesterday
import time
from datetime import datetime, timedelta
import schedule

from instagrapi import Client

def upload():
    file_location = return_planner_img()
    yesterday = datetime.now() - timedelta(1)
    today_date = yesterday.strftime("%y%m%d")

    media = client.photo_upload(
        file_location,
        f'{today_date} #공스타'
    )

    print('uploaded : ' + today_date)

if __name__ == '__main__':
    client = Client()
    client.login($INSTAGRAM-ID, $INSTAGRAM-PASSWORD)

    upload()

    schedule.every().day.at('02:00').do(upload)

    while True:
        schedule.run_pending()
        time.sleep(1)
