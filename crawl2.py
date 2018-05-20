from urllib.parse import urlencode
import requests
import csv
#base_url = 'https://www.thebump.com/real-answers/v1/categories/33/questions?'
base_url = 'https://www.thebump.com/real-answers/v1/categories/'
headers ={
    'authority': 'www.thebump.com',
    'referer': 'https://www.thebump.com/real-answers/stages/first-trimester',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',

}



def get_total(url_json):
    return url_json["total"]


#连接
def get_page(page, page_num, page_size):
    page_num = "" + str(page_num)
    page= "" + str(page)
    params = {
        "page_num" : page_num,
        "page_size" : page_size,
        "filter" : "ranking"
    }
    url_page = base_url + page
    url = base_url + page + "/questions?" + urlencode(params)
    try:
        response_page = requests.get(url_page)
        response_url = requests.get(url)
        if response_page.status_code == 200 and response_url.status_code == 200:
            page_json = response_page.json()
            url_json = response_url.json()
            return page_json, url_json
    except requests.ConnectionError as e:
        print('Error', e.args)



# 取值
def parse_page(page_json, url_json):
    if page_json and url_json:
        items = url_json.get("questions")
        for item in items:
            questions = {}
            questions["title"] = item.get("title")
            questions["create_at"] = item.get("created_at")
            questions["user_id"] = item.get("user_id")
            questions["user_name"] = item.get("user")["username"]
            if page_json["id"] <= 35 and page_json["id"] >= 33:
                questions["category_name"] = "PREGNANCY"
                questions["subcategory_name"] = page_json.get("name")
            elif page_json["id"] >= 37 and page_json["id"] <= 47:
                questions["category_name"] = "PARENTING"
                questions["subcategory_name"] = page_json.get("name")
            elif page_json["id"] == 23 or page_json["id"] == 24:
                questions["category_name"] = "PREGNANCY"
                questions["subcategory_name"] = page_json.get("name")
            yield questions




#通过total判定爬取
if __name__ == "__main__":
    with open("f:/3.csv", 'w', newline='',  encoding="utf-8") as f:
        fieldnames = ["category_name", "subcategory_name", "title", "create_at", "user_id", "user_name"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for i in range(33, 48):   #分类的id号
            num = 1000
            page = i
            page_num = 1
            if get_page(page, page_num, 1):
                page_json, url_json = get_page(page, page_num, 1)
                total = get_total(url_json)
                while total > 0:
                    if get_page(page, page_num, 1):
                        page_json, url_json = get_page(page, page_num, num)
                        results = parse_page(page_json, url_json)
                        for result in results:
                            writer.writerow(result)
                        if total - num > 0:
                            total -= num

                        elif total - num // 10 > 0:
                            total -= num // 10
                            num //= 10

                            if num == 0:
                                break
                        else:
                            break
                        page_num += 1
                    else:
                        continue
            else:
                 continue
