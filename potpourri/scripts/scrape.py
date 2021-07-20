from lxml.html.soupparser import fromstring
from src.scripts.keyword_extraction import kword
import time

def scrape(html_body, url, tags_to_get, attrs_keywords_to_get, get_keywords=False):
    start = time.time()
    root = fromstring(html_body)

    results = {"url": url}
    
    body = root.xpath("//body/descendant::*/text()")
    title = root.xpath("//title/text()")

    results["body"] = {"whole": body, "keywords": None}
    results["title"] = {"whole": title, "keywords": None}

    if get_keywords:
        keywords_body = kword(body)
        keywords_title = kword(title)

        results["body"]["keywords"] = keywords_body
        results["title"]["keywords"] = keywords_title

    results["hrefs"] = root.xpath("//a/@href")
    results["meta_desc"] = root.xpath("//meta[@name = 'description']/@content")
    results["meta_keywords"] = root.xpath("//meta[@name = 'keywords']/@content")
    results["meta_author"] = root.xpath("//meta[@name = 'author']/@content")
    results["image_alts"] = root.xpath("//img/@alt")
    results["bolds"] = root.xpath("//b/text()")
    results["italics"] = root.xpath("//i/text()")
    results["lists"] = root.xpath("//ul/text()")
    results["strongs"] = root.xpath("//strong/text()")
    results["h1"] = root.xpath("//h1/text()")
    results["h2"] = root.xpath("//h2/text()")
    results["h3"] = root.xpath("//h3/text()")
    results["h4"] = root.xpath("//h4/text()")
    results["h5"] = root.xpath("//h5/text()")
    results["h6"] = root.xpath("//h6/text()")

    results["html"] = html_body

    elements_body = root.xpath("//*[local-name()='p' or local-name()='li'\
                or local-name()='h1' or local-name()='h2' or local-name()='h3' or local-name()='h4'\
                or local-name()='h5' or local-name()='h6' or local-name()='span']/text()")

    elements_ret = [r.strip().strip("\n") for r in elements_body if len(r) > 1]

    results["classic"] = ";\n".join(elements_ret)

    results["lengths"] = {"html_length": len(html_body), 
    "body_length": len(body),
     "title_length": len(title)}

    results["custom_tags"] = {}
    for tag, attributes in tags_to_get.items():
        results["custom_tags"][tag] = {}
        for attr in attributes:
            try:        
                results["custom_tags"][tag][attr] = root.xpath(f"//{tag.name}/{attr}")
                results["custom_tags"][tag][f"{attr}-descendents"] = root.xpath(f"//{tag.name}/descendant::*/{attr}")
            except:
                results["custom_tags"][tag][attr] = None
                results["custom_tags"][tag][f"{attr}-descendents"] = None

    results["custom_attrs"] = {}
    for attr, kws in attrs_keywords_to_get.items():
        results["custom_attrs"][attr] = {}
        for kw in kws:
            try:        
                results["custom_attrs"][attr][kw] = root.xpath(f"//*[contains('{attr}', '{kw}')]/text()")
                results["custom_attrs"][attr][f"{kw}-descendents"] = root.xpath(f"//*[contains('{attr}', '{kw}')]/descendant::*/text()")
            except:
                results["custom_attrs"][attr][kw] = None
                results["custom_attrs"][attr][f"{kw}-descendents"] = None

    end = time.time()

    results["time"]  = end - start

    return results