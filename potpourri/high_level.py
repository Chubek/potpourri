from .concurrent_runner import ConcurrentRunner


def search_and_scrape_single(scraper, psearch, keyword, custom_tags={}, custom_attrs={}, search_kw=True, refer_google=False):
    psearch.search_single_kw(keyword)
    urls = psearch.get_urls_only_single(keyword)
    descriptions = psearch.get_descs_only_single(keyword)
    scraper.scrape_multiple(urls, custom_tags=custom_tags, custom_attrs=custom_attrs, search_kw=search_kw, refer_google=refer_google)    
    df = scraper.make_pandas_df(urls, descriptions)

    return df