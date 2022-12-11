# notion-auto-planner

Automatic study planner using Notion | [instagram](https://www.instagram.com/study_bss/)

## Settings

### Notion

<img src="https://user-images.githubusercontent.com/55339366/206874801-8372fd03-9d25-41a9-bd6f-1b669f45543a.png" width="50%" height="50%">
범위, 과목, 공시 등을 인자로 갖는 Notion DB 구축

### Instagram

<img src="https://user-images.githubusercontent.com/55339366/206913890-d31bbcce-c711-4542-ad59-532549aee567.png" width="50%" height="50%">
프로페셔널 계정으로 전환

### Python

```ruby
client = Client()
client.login($ID, $PASSWORD)

upload()

schedule.every().day.at('02:00').do(upload)

while True:
    schedule.run_pending()
    time.sleep(1)
```
instagrapi Client로 로그인, 일정 시간 주기로 업로드

## Sample
<img src="https://user-images.githubusercontent.com/55339366/206874749-65d4ad9f-2f11-485e-9e55-471f90b877d1.png" width="50%" height="50%">

## References
- [notion sample template](https://ubiquitous-polka-b43.notion.site/Study-Planner-5ceb48ac502242ab8c68452f9563fd59)
- [notion api reference](https://developers.notion.com/reference/intro)
- [json formatter](https://jsonformatter.curiousconcept.com/#)

## Dependencies
- Notion: 22-06-28
- [PIL](https://github.com/python-pillow/Pillow)
- requests, json
- [schedule](https://github.com/dbader/schedule)
- [instagrapi](https://github.com/adw0rd/instagrapi)

### TODO
---
- ~auto instagram upload~
- add to-do, memos
-
