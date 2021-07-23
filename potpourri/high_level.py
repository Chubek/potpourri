from .concurrent_runner import ConcurrentRunner
import pandas as pd

def search_and_scrape_single(scraper, psearch, keyword, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_single_kw(keyword)
    urls = psearch.get_urls_only_single(keyword)
    descriptions = psearch.get_descs_only_single(keyword)
    scraper.scrape_multiple(urls, custom_tags=custom_tags, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    
    df = scraper.make_pandas_df(urls, descriptions)

    return df

def search_and_scrape_multiple(scraper, psearch, keywords, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_multiple_kw(keywords)
    urls = psearch.get_urls_only_single(keywords)
    descriptions = psearch.get_descs_only_single(keywords)

    urls_summed = sum(urls, [])
    descriptions_summed = sum(descriptions, [])

    scraper.scrape_multiple(urls_summed, custom_tags=custom_tags, custom_attrs=custom_attrs, get_kw=search_kw, google_refer=refer_google)    
    df = scraper.make_pandas_df(urls_summed, descriptions_summed)

    return df

def run_parallel(funcs, args):
    crunner = ConcurrentRunner()

    if len(funcs) != len(args):
        funcs_list = [funcs[0] for _ in range(len(args))]

    dict_func_args = dict(zip(funcs_list, args))

    results = crunner.run_funcs_parallel(dict_func_args)

    return pd.concat(list(results.values()), ignore_index=True)
    
def run_concurrent(funcs, args):
    crunner = ConcurrentRunner()

    if len(funcs) != len(args):
        funcs_list = [funcs[0] for _ in range(len(args))]

    dict_func_args = dict(zip(funcs_list, args))

    results = crunner.run_funcs_concurrent(dict_func_args)

    return pd.concat(list(results.values()), ignore_index=True)
    