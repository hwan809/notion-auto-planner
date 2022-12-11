import requests, json
import time
import random
from datetime import datetime, timedelta

from PIL import Image, ImageFont, ImageDraw

token = 'secret_BMuvxz0YRJkx18w6Zhghz2vnkxWkRb8zg6fIVnDRRcO'
headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    
}
database_id = 'a588c20b16a74c54ab364040d5db5a6c'

read_url = f"https://api.notion.com/v1/databases/{database_id}/query"

TAG_TIME = '공시 (m)'
TAG_FINISHED = '완료'
TAG_RANGE = '범위'

TAG_CHECKBOX = 'checkbox'
TAG_NUMBER = 'number'
TAG_TITLE = 'title'
TAG_TEXT = 'text'
TAG_CONTENT = 'content'
TAG_RELATION = 'relation'
TAG_ID = 'id'

TAG_BIG_PLAN = '큰 계획'

class Plan:
    def __init__(
        self, 
        range,
        big_plan,
        subject,
        subject_type,
        emoji,
        time : int,
        has_finished: bool
    ):

        self.has_finished = has_finished
        self.range = range
        self.big_plan = big_plan
        self.subject = subject
        self.subject_type = subject_type
        self.emoji = emoji
        self.time = time

    def print(self):
        return self.has_finished, self.range, self.big_plan, self.subject, self.subject_type, self.emoji, self.time

def yesterday(frmt='%Y-%m-%d', string=True):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday

def minutes_to_text(minutes):
    hour = minutes // 60
    minute = minutes % 60

    return f'{hour}H {minute}M'

def get_databases():
    databases = []
    payload = {}

    has_more = True
    counter = 0

    while has_more:
        res = requests.post(read_url, json=payload, headers=headers)
        res_json = json.loads(res.text)
        databases.append(res_json)

        if res_json['has_more'] == True:
            next_cursor = res_json['next_cursor']
            payload = {
                "start_cursor": next_cursor
            }
        else:
            has_more = False

        counter += 1
        
    return databases

def get_todays(databases):
    today_databases = []

    for database in databases:
        for result in database["results"]:
            try:
                if result["properties"]["계획 날짜"]["date"]["start"] == yesterday():
                    today_databases.append(result)
            except:
                pass
    return today_databases

def get_plan_datas(today_databases):
    today_plans = []

    for today_database in today_databases:
        today_database = today_database['properties']

        study_range = today_database[TAG_RANGE][TAG_TITLE][0][TAG_TEXT][TAG_CONTENT]
        study_time = today_database[TAG_TIME][TAG_NUMBER]
        study_finished = today_database[TAG_FINISHED][TAG_CHECKBOX]
        
        study_big_plan_id = today_database[TAG_BIG_PLAN][TAG_RELATION][0][TAG_ID]

        url = f"https://api.notion.com/v1/pages/{study_big_plan_id}"
        res = requests.get(url, headers=headers)
        study_big_plan_json = json.loads(res.text)["properties"]

        big_plan_name = study_big_plan_json["이름"][TAG_TITLE][0][TAG_TEXT][TAG_CONTENT]

        study_subject_id = study_big_plan_json["공부"][TAG_RELATION][0][TAG_ID]

        url = f"https://api.notion.com/v1/pages/{study_subject_id}"
        res = requests.get(url, headers=headers)
        study_subject_json = json.loads(res.text)

        study_subject_name = study_subject_json["properties"]["이름"][TAG_TITLE][0][TAG_TEXT][TAG_CONTENT]
        study_subject_type = study_subject_json["properties"]["과목"]["select"]["name"]
        study_subject_emoji = study_subject_json["icon"]["emoji"]

        today_plan = Plan(study_range, big_plan_name, study_subject_name, study_subject_type, study_subject_emoji, study_time, study_finished)
        today_plans.append(today_plan)

        #print(today_plan.print())
    
    return today_plans

def create_planner_img(plans):
    today = time.strftime('%y.%m.%d %a')
    d_day = 19

    # TODO - get D-day 2f5ccc1cbfdf43caa5d9ec4a40e1f593
    study_time_sum = 0

    for plan in plans:
        if plan.time != None:
            study_time_sum += plan.time

    background = Image.open(f'planner_png/{random.randint(1, 4)}.png').convert("RGB")
    
    font_2_B = ImageFont.truetype('fonts/2_B.ttf', 125)
    font_2_L = ImageFont.truetype('fonts/2_L.ttf', 60)

    font_1_B = ImageFont.truetype('fonts/Cafe24Ssurround.ttf', 55)
    font_1_L = ImageFont.truetype('fonts/Cafe24Ssurroundair.ttf', 35)

    draw = ImageDraw.Draw(background)

    draw.text((155, 195), today, (0, 0, 0), font=font_2_B)
    draw.text((1030, 195), f'D-{d_day}', (0, 0, 0), font=font_2_B)
    draw.text((1320, 250), '방학식', (0, 0, 0), font=font_2_L)
    draw.text((1030, 405), minutes_to_text(study_time_sum), (0, 0, 0), font=font_2_B)
    
    plans = sorted(plans, key=lambda plan: plan.subject_type, reverse=True)

    subject_type = ''
    now_pointer = (150, 695)

    for plan in plans:
        now_type = plan.subject_type
        
        if plan.subject_type != subject_type:
            now_pointer = (now_pointer[0], now_pointer[1] + 70)
            draw.text((now_pointer[0], now_pointer[1]), plan.subject_type, (0, 0, 0), font=font_1_B)
            
            subject_type = now_type

        draw.text((now_pointer[0] + 130, now_pointer[1] + 10), plan.subject + ' : ' + plan.range, (0, 0, 0), font=font_1_L)

        if plan.has_finished:
            draw.text((now_pointer[0] + 700, now_pointer[1]), 'O', (80, 200, 40), font=font_1_B)
        else:
            draw.text((now_pointer[0] + 700, now_pointer[1]), 'X', (200, 40, 80), font=font_1_B)

        now_pointer = (now_pointer[0], now_pointer[1] + 70)
        
    #STICKERS
    time_6h = Image.open('stickers/fire.png').convert('RGBA').rotate(15)
    smile = Image.open('stickers/3.png').convert('RGBA')

    if study_time_sum > 60 * 6:
        background.paste(time_6h, (1350, 320), time_6h)
    background.paste(smile, (155, 395), smile)

    f_location = f'my_planner/{time.strftime("%Y-%m-%d")}.jpg'
    background.save(f_location)
    return f_location

def return_planner_img():
    databases = get_databases()
    today_databases = get_todays(databases)
    plans = get_plan_datas(today_databases) 

    img = create_planner_img(plans)
    return img

if __name__ == '__main__':
    return_planner_img()

    pass