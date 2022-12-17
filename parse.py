# parse.py

import requests
import json
import datetime

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
	"X-Requested-With": "XMLHttpRequest"
}

def get_data():
	start_time = datetime.datetime.now()
	url = "https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort%5Bprice%5D=asc&PAGEN_1=1"
	r = requests.get(url=url, headers=headers)

	#with open("index.html", "w") as file:
	#	file.write(r.text)
	#print(r.json())

	#with open("data.json", "w") as file:
	#	json.dump(r.json(), file, indent=4, ensure_ascii=False)


	pages_count = r.json()["pagesCount"]
	
	data_list = []

	for page in range(1, pages_count + 1):
		url = f"https://roscarservis.ru/catalog/legkovye/?set_filter=Y&sort%5Bprice%5D=asc&PAGEN_1={page}"
		r = requests.get(url=url, headers=headers)
		data = r.json()
		items = data["items"]
		possible_stores = ["discountStores", "externalStores", "commonStores"]

		for item in items:
			total_amount = 0

			item_id = item["id"]
			item_name = item["name"]
			item_url = f'https://roscarservis.ru{item["url"]}'
			item_season = item["season"]
			item_price = item["price"]
			item_image = f'https://roscarservis.ru{item["imgSrc"]}'

			stores = []

			for ps in possible_stores:
				if ps in item:
					if item[ps] is None or len(item[ps]) < 1:
						continue
					else:
						for store in item[ps]:
							store_name = store["STORE_NAME"]
							store_price = store["PRICE"]
							store_amount = store["AMOUNT"]
							total_amount += int(store["AMOUNT"]) 

							stores.append(
								{
									"store_name": store_name,
									"store_price": store_price,
									"store_amount": store_amount

								}
							)

			data_list.append(
				{
					"name": item_name,
					"price": item_price,
					"url": item_url,
					"img_url": item_image,
					"stores": stores,
					"total_amount": total_amount
				})
		print(f"[INFO] Обработал {page}/{pages_count}")

	cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
	with open(f"data_{cur_time}.json", "a") as file:
		json.dump(data_list, file, indent=4, ensure_ascii=False)
	diff_time = datetime.datetime.now() - start_time
	print(diff_time)

def main():
	get_data()


if __name__ == '__main__':
		main()	
