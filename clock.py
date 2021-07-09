from apscheduler.schedulers.blocking import BlockingScheduler
from scrapers.future_weather_scraper import scrape


sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=3)
def weather_scraper():
    scrape()

sched.start()