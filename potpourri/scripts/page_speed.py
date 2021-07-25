import requests
import os
import time
import concurrent.futures

def get_page_speed(url):
    req = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={os.environ["GOOGLE_API_KEY"]}')

    return req.json()



def get_page_speed_fas(url, res):
    print(f"Getting speed for {url}")
    res[url] = get_page_speed(url)
    

async def get_multiple_speeds_async(urls):
    res = {}

    chunks = [urls[x:x + 6] for x in range(0, len(urls), 6)]

    for task_chunk in chunks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:

            func_results = {executor.submit(get_page_speed_fas, url_chunk, res): url_chunk for url_chunk in task_chunk}

            for future in concurrent.futures.as_completed(func_results):
                arg = func_results[future]
                try:
                    data = future.result()                   
                    
                except Exception as exc:
                    print('%r generated an exception: %s' % (arg, exc))
                else:
                    print('%r page is %d bytes' % (arg, len(data)))

            time.sleep(0.5)


    return res
