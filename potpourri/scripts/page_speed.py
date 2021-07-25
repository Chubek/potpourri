import requests
import os
import asyncio
import time

def get_page_speed(url):
    req = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={os.environ["GOOGLE_API_KEY"]}')

    return req.json()



def get_page_speed_fas(url, res):
    res[url] = get_page_speed(url)
    

async def get_multiple_speeds_async(urls):
    res = {}

    tasks = []

    for url in urls:
        tasks.append(asyncio.create_task(get_page_speed_fas(url, res)))

    chunks = [tasks[x:x + 4] for x in range(0, len(tasks), 4)]

    for task_chunk in chunks:
        if len(task_chunk) == 4:
            await task_chunk[0]
            await task_chunk[1]
            await task_chunk[2]
            await task_chunk[3]
        elif len(task_chunk) == 3:
            await task_chunk[0]
            await task_chunk[1]
            await task_chunk[2]
        elif len(task_chunk) == 2:
            await task_chunk[0]
            await task_chunk[1]
        elif len(task_chunk) == 1:
            await task_chunk[0]
        else:
            continue

        time.sleep(0.25)


    return res
