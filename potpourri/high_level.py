from potpourri.scripts.scrape import scrape
import concurrent.futures
import pandas as pd

def search_and_scrape_single(scraper, psearch, keyword, parallel=True, max_worker=6, retry=True, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_single_kw(keyword)
    urls = psearch.get_urls_only_single(keyword)
    descriptions = psearch.get_descs_only_single(keyword)

    if parallel:
        scraper.scrape_multiple_parallel(urls, custom_tags=custom_tags, max_worker=max_worker, retry=retry, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    
    else:
        scraper.scrape_multiple(urls, custom_tags=custom_tags, retry=retry, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    

    df = scraper.make_pandas_df(urls, descriptions)

    return df

def search_and_scrape_single_wm(scraper, psearch, keyword, parallel=True, max_worker=6, max_worker_speed=12, retry=False, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_single_kw(keyword)
    urls = psearch.get_urls_only_single(keyword)
    descriptions = psearch.get_descs_only_single(keyword)

    if parallel:
        scraper.scrape_multiple_parallel(urls, custom_tags=custom_tags, max_worker=max_worker, retry=retry, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    
    else:
        scraper.scrape_multiple(urls, custom_tags=custom_tags, retry=retry, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    

    scraper.request_own_page_rank_multiple(urls)
    scraper.request_own_page_speed_multiple(urls, max_worker=max_worker_speed)
    df = scraper.make_pandas_df(urls, descriptions)

    return df

def search_and_scrape_multiple(scraper, psearch, keywords, parallel=True, max_worker=6, retry=False, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_multiple_kw(keywords)
    urls = psearch.get_urls_only_single(keywords)
    descriptions = psearch.get_descs_only_single(keywords)

    urls_summed = sum(urls, [])
    descriptions_summed = sum(descriptions, [])

    if parallel:   
        scraper.scrape_multiple_parallel(urls_summed, retry=retry, max_worker=max_worker, custom_tags=custom_tags, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    
    else:
        scraper.scrape_multiple(urls_summed, retry=retry, custom_tags=custom_tags, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    

    df = scraper.make_pandas_df(urls_summed, descriptions_summed)

    return df

def search_and_scrape_multiple_wm(scraper, psearch, keywords, parallel=True, max_worker=6, max_worker_speed=12, retry=False, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_multiple_kw(keywords)
    urls = psearch.get_urls_only_single(keywords)
    descriptions = psearch.get_descs_only_single(keywords)

    urls_summed = sum(urls, [])
    descriptions_summed = sum(descriptions, [])

    if parallel:
        scraper.scrape_multiple_parallel(urls_summed, retry=retry, max_worker=max_worker, custom_tags=custom_tags, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google) 
    else:
        scraper.scrape_multiple(urls_summed, retry=retry, custom_tags=custom_tags, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google) 

    scraper.request_own_page_rank_multiple(urls)
    scraper.request_own_page_speed_multiple(urls, max_worker=max_worker_speed)

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

    