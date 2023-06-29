import requests 
from bs4 import BeautifulSoup
import json
import csv
from time import sleep


url = "https://www.calories.info/"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
}

req = requests.get(url, headers)
src = req.text


with open("index.html", "w") as file:
    file.write(src)

with open("index.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

links = soup.find_all(class_="calorie-link")

all_categories_dict = {}

for i in links:
    item_text = i.find("h3").text
    item_href = i.get("href")
    all_categories_dict[item_text] = item_href



# # Step with making json file

with open("all_categories_dict.json", "w") as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open("all_categories_dict.json") as file:
    all_categories = json.load(file)

iterations_count = len(all_categories) - 1
count = 0
for category_name, category_href in all_categories.items():
    rep = [",", " ", ".", "(", ")"]

    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_href, headers = headers)
    src = req.text

    with open(f"data_templates/{category_name}.html", "w") as file:
        file.write(src)

    with open(f"data_templates/{category_name}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # Get headers
    table_head = soup.find("thead").find_all("td")
    product = table_head[0].text
    serving = table_head[1].text
    calories = table_head[2].text


    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow((
            product,
            serving,
            calories,
        ))

    # get data

    products_data = soup.find_all(class_ = "kt-row")

    product_info = []

    for item in products_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        serving = product_tds[1].text
        calories = product_tds[4].text

        product_info.append({
            "title": title,
            "serving": serving,
            "calories": calories,
        })
        
        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow((
                title,
                serving,
                calories,
            ))

    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"Iteration {count}. {category_name} written..")
    iterations_count -= 1

    if iterations_count == 0:
        print("Work is done.")
        break
    
    
    sleep(1)

