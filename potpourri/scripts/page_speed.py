import requests
import os
import time
import concurrent.futures

def get_page_speed(url, strategy="desktop"):
    req = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}&key={os.environ["GOOGLE_API_KEY"]}')
    
    json = req.json()


    return {"numericValue": json['lighthouseResult']['audits']['bootup-time']['numericValue'], 
              "score": json['lighthouseResult']['audits']['bootup-time']['score']  }



def get_page_speed_fas(url, res, strategy='desktop'):
    print(f"Getting speed for {url}")
    res[url] = get_page_speed(url, strategy=strategy)
    

def get_multiple_speeds_async(urls, num_worker=12, strategy="desktop"):
    res = {}

    chunks = [urls[x:x + num_worker] for x in range(0, len(urls), num_worker)]

    for task_chunk in chunks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_worker) as executor:

            func_results = {executor.submit(get_page_speed_fas, url_chunk, res, strategy): url_chunk for url_chunk in task_chunk}

            for future in concurrent.futures.as_completed(func_results):
                arg = func_results[future]
                try:
                    _ = future.result()                   
                    
                except Exception as exc:
                    print('%r generated an exception: %s' % (arg, exc))

            time.sleep(0.25)


    return res
