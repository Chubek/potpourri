import threading
import concurrent.futures
import pandas as pd

def search_and_scrape_single(scraper, psearch, keyword, retry=True, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_single_kw(keyword)
    urls = psearch.get_urls_only_single(keyword)
    descriptions = psearch.get_descs_only_single(keyword)
    scraper.scrape_multiple(urls, custom_tags=custom_tags, retry=retry, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    
    df = scraper.make_pandas_df(urls, descriptions)

    return df

def search_and_scrape_multiple(scraper, psearch, keywords, retry=True, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_multiple_kw(keywords)
    urls = psearch.get_urls_only_single(keywords)
    descriptions = psearch.get_descs_only_single(keywords)

    urls_summed = sum(urls, [])
    descriptions_summed = sum(descriptions, [])

    scraper.scrape_multiple(urls_summed, retry=retry, custom_tags=custom_tags, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    
    df = scraper.make_pandas_df(urls_summed, descriptions_summed)

    return df

def run_parallel(func, args, max_worker=5):
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:

        func_results = {executor.submit(func, *arg): arg for arg in args}

        for future in concurrent.futures.as_completed(func_results):
            arg = func_results[future]
            try:
                data = future.result()
                res.append(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (arg, exc))
            else:
                print('%r page is %d bytes' % (arg, len(data)))

    return pd.concat(res, ignore_index=True)

    