# !/bin/env python3

import requests, json, csv, pandas, asyncio, aiohttp
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

rrurl = 'https://reqres.in/api/users'
results_per_page = 3

#to check for pagination
def make_request_url(results_per_page, current_page_number):
    return (
        "https://reqres.in/api/users"
        + "?per_page="
        + str(results_per_page)
        + "&page="
        + str(current_page_number)
    )

def make_url_list(results_per_page, current_page_number, total_pages):
    urls = []
    for i in range(1,total_pages+1):
        urls.append(make_request_url(results_per_page,i))
    return urls

def grab_total_pages(results_per_page):
    with requests.session() as s:
        url = make_request_url(results_per_page, 1)
        resp = s.get(url, verify=False)
    
    if resp.status_code != 200:
        raise Exception(resp.status_code)
    
    return int((resp.json())["total_pages"])

async def grab_json(url,session):   
    async with session.get(url) as r:
        raw = await r.json()
        return raw.get("data")

async def gather_data(url_list):
     async with aiohttp.ClientSession() as cs:
        tasks = []
        for page in url_list:
            tasks.append(grab_json(page,cs))
        results = await asyncio.gather(*tasks)
        return results

# def get_result(current_page_number):
#     with requests.session() as s:
#         url = make_request_url(results_per_page, current_page_number)
#         resp = s.get(url, verify=False)

#     if resp.status_code != 200:
#         raise Exception(resp.status_code)

#     raw = resp.json() 
#     data = raw.get("data")  #list

#     if (raw["page"] == raw["total_pages"]):
#          return data

    # return data + get_result(current_page_number + 1)  # concat lists

# def puttocsv(datablock):
#     with open("output.csv","w",newline="") as f:  
#         title = "id,email,first_name,last_name,avatar".split(",") # quick hack
#         cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         cw.writeheader()
#         cw.writerows(datablock)


def pandastohtml(datablock):
    df = pandas.DataFrame(datablock)
    with open('mbchal.html', 'w') as f:
        df.to_html(buf=f,escape=False)
    
def main():
    
    total_pages = grab_total_pages(results_per_page)
    url_list = make_url_list(results_per_page,1,total_pages)
    datablock = asyncio.run(gather_data(url_list=set(url_list)))
    flat_datablock = [item for sublist in datablock for item in sublist]
    for block in flat_datablock:
        block['avatar'] = '<img src="' + block['avatar'] + '" width="60" >'
    pandastohtml(flat_datablock)
 
    # Then you can print the data or save it to a file

if __name__ == "__main__":
    # Now run the driver function
    datablock = [] 
    main()
