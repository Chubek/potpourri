from lxml.html.soupparser import fromstring
from .keyword_extraction import kword
from .page_rank import get_page_ranks
from .utils import find_all_words, filter_list, flatten_list, split_internal_external, parse_url
import time

def scrape(html_body, url, tags_to_get, attrs_keywords_to_get, get_keywords=False):
    start = time.time()
    root = fromstring(html_body)

    results = {"url": {"address": url, "parsed": parse_url(url),
            "page_speed": "Not requsted yet", 
            "page_rank": "Not requsted yet"}}
    
    body = " ".join(filter_list(root.xpath("//body/descendant::*/text()")))
    title = root.xpath("//title/text()")[0]

    results["body"] = {"whole": body, "num_words": find_all_words(body), "keywords": None}
    results["title"] = {"whole": title, "num_words": find_all_words(title), "keywords": None}

    if get_keywords:
        keywords_body = kword(body)
        keywords_title = kword(title)

        results["body"]["keywords"] = keywords_body
        results["title"]["keywords"] = keywords_title

    results["links"] = {}

    results["links"]["hrefs"] = filter_list(root.xpath("//a/@href"))
    results["links"]["internal_urls"], results["links"]["external_urls"] = split_internal_external(url, results["links"]["hrefs"])
    results["links"]["internal_urls_speeds"] = "Not Yet Requested"
    results["links"]["external_urls_speeds"] = "Not Yet Requested"
    results["links"]["internal_urls_ranks"] = "Not Yet Requested"
    results["links"]["external_urls_ranks"] = "Not Yet Requested"


    results["meta_charset"] = filter_list(root.xpath("//meta/@charset"))
    results["meta_desc"] = filter_list(flatten_list([filter_list(root.xpath("//meta[@name = 'description']/@content")), 
                    root.xpath("//meta[@name = 'Description']/@content")]))
    results["meta_keywords"] = filter_list(flatten_list([filter_list(root.xpath("//meta[@name = 'keywords']/@content")), 
                    root.xpath("//meta[@name = 'Keywords']/@content")]))
    results["meta_author"] = filter_list(flatten_list([filter_list(root.xpath("//meta[@name = 'author']/@content")), 
                    root.xpath("//meta[@name = 'Author']/@content")]))
    results["image_alts"] = filter_list(root.xpath("//img/@alt"))
    results["bolds"] = filter_list(flatten_list([root.xpath("//b/text()"), root.xpath("//b/descendant::*/text()")]))
    results["italics"] = filter_list(flatten_list([root.xpath("//i/text()"), root.xpath("//i/descendant::*/text()")]))
    results["lists"] = filter_list(flatten_list([root.xpath("//ul/text()"), root.xpath("//ul/descendant::*/text()")]))
    results["strongs"] = filter_list(flatten_list([root.xpath("//strong/text()"), root.xpath("//strong/descendant::*/text()")]))
    results["h1"] = filter_list(flatten_list([root.xpath("//h1/text()"), root.xpath("//h1/descendant::*/text()")]))
    results["h2"] = filter_list(flatten_list([root.xpath("//h2/text()"), root.xpath("//h2/descendant::*/text()")]))
    results["h3"] = filter_list(flatten_list([root.xpath("//h3/text()"), root.xpath("//h3/descendant::*/text()")]))
    results["h4"] = filter_list(flatten_list([root.xpath("//h4/text()"), root.xpath("//h4/descendant::*/text()")]))
    results["h5"] = filter_list(flatten_list([root.xpath("//h5/text()"), root.xpath("//h5/descendant::*/text()")]))
    results["h6"] = filter_list(flatten_list([root.xpath("//h6/text()"), root.xpath("//h6/descendant::*/text()")]))

    try:
        results["html"] = html_body.decode("utf-8")
    except:
        try:
            results["html"] = html_body.decode(results["meta_charset"][0])
        except:
            results["html"] = str(html_body)


    elements_body = root.xpath("//*[local-name()='p' or local-name()='li'\
                or local-name()='h1' or local-name()='h2' or local-name()='h3' or local-name()='h4'\
                or local-name()='h5' or local-name()='h6' or local-name()='span']/text()")

    elements_ret = filter_list([r.strip().strip("\n") for r in elements_body if len(r) > 1])

    results["classics"] = ";\n".join(elements_ret)

    results["lengths"] = {"html_length": len(html_body), 
    "body_length": len(body),
     "title_length": len(title)}

    results["custom_tags"] = {}
    for tag, attributes in tags_to_get.items():
        results["custom_tags"][tag] = {}
        for attr in attributes:
            try:        
                results["custom_tags"][tag][attr] = filter_list(root.xpath(f"//{tag.name}/{attr}"))
                results["custom_tags"][tag][f"{attr}-descendents"] = filter_list(root.xpath(f"//{tag.name}/descendant::*/{attr}"))
            except:
                results["custom_tags"][tag][attr] = None
                results["custom_tags"][tag][f"{attr}-descendents"] = None

    results["custom_attrs"] = {}
    for attr, kws in attrs_keywords_to_get.items():
        results["custom_attrs"][attr] = {}
        for kw in kws:
            try:        
                results["custom_attrs"][attr][kw] = filter_list(root.xpath(f"//*[contains('{attr}', '{kw}')]/text()"))
                results["custom_attrs"][attr][f"{kw}-descendents"] = filter_list(root.xpath(f"//*[contains('{attr}', '{kw}')]/descendant::*/text()"))
            except:
                results["custom_attrs"][attr][kw] = None
                results["custom_attrs"][attr][f"{kw}-descendents"] = None

    end = time.time()

    results["time"]  = end - start

    return results