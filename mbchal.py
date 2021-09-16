# !/bin/env python3

import requests, json, csv, pandas
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

rrurl = 'https://reqres.in/api/users'
results_per_page = 100

#to check for pagination
def make_request_url(results_per_page, current_page_number):
    return (
        "https://reqres.in/api/users"
        + "?per_page="
        + str(results_per_page)
        + "&page_number="
        + str(current_page_number)
    )

def get_result(current_page_number):
    with requests.session() as s:
        url = make_request_url(results_per_page, current_page_number)
        resp = s.get(url, verify=False)

    if resp.status_code != 200:
        raise Exception(resp.status_code)

    raw = resp.json()  #dict
    data = raw.get("data")  #list

    if len(data) < results_per_page:
        return data

    return data + get_result(current_page_number + 1)  # concat lists

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
    datablock = get_result(1) #list of jsons
    for block in datablock:
        block['avatar'] = '<img src="' + block['avatar'] + '" width="60" >'
    pandastohtml(datablock)
 
    # Then you can print the data or save it to a file

if __name__ == "__main__":
    # Now run the driver function
    main()
