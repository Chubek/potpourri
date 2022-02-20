from googleapiclient.discovery import build
import os



def search_web(term, res_num, step):
  results = []

  for start in range(1, 101, step):
    service = build("customsearch", "v1",
            developerKey=os.environ["GOOGLE_API_KEY"])
    res = service.cse().list(
      q=term,
      cx=os.environ["GOOGLE_CX"],
      start=start, num=res_num
    ).execute()

    results.append(res)

  
  
  ret = []
  for res in results:  
    try:
      _ = res['items'][0]['link']
    except:
      continue
    
    for r in res['items']:
      if r['link'].strip().split(".")[-1] == "pdf":
        continue
      if 'snippet' in r:
        ret.append((r['link'].strip().strip("\n"), r['snippet'].strip().strip("\n")))
      else:
        ret.append((r['link'].strip().strip("\n"), "No Snippet!"))

  return ret