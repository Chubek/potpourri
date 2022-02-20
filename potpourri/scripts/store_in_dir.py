import json
import os
import re
from datetime import datetime

def store_in_dir(dir, identifier, res):
    site_np = re.sub(r"https:\/\/|http:\/\/|\/", "", res["url"])

    dt = datetime.now()

    if not os.path.exists(os.path.join(dir, site_np)):
        os.makedirs(os.path.join(dir, site_np))

    path = os.path.join(dir, f"site_np-{identifier}", dt.strftime("%d-%b-%Y (%H:%M:%S.%f)") + ".json")



    with open(path) as jf:
        json.dump(res, jf, indent=8)


