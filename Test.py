import os
import concurrent.futures
import time
import random

from Config import Config
import Main


#Get all of the Users
with concurrent.futures.ThreadPoolExecutor(max_workers=(len(Config.User['Users']))) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(Main.Facebook_Group,User): User for User in Config.User['Users']}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            err = ""
            print('%r generated an exception: %s' % (url, exc))
