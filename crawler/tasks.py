from celery import shared_task

from crawler.spider import Spider


@shared_task
def create_crawling_task(url):
    spider = Spider(url)
    return spider.process()
