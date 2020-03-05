import json
from urllib.request import urlopen

from bs4 import BeautifulSoup

from urllist import naver_list


def fetch_url(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup


def naver_store(soup):
	form = soup.find('form', {'class': '_sale_info'})

	# 이름
	name = form.find('dt', {'class': 'prd_name'}).find('strong').get_text().strip()

	# 가격
	price = form.find('strong', {'class': 'info_cost'}).find_all('span', {'class': 'thm'})
	if len(price) == 2:
		price = price[1].get_text().strip()
	else:
		price = price[0].get_text().strip()
	price = int(price.replace(',', ''))

	# 배달비
	delivery_cost = form.find('span', {'class': '_deliveryBaseFeeAreaValue'}).get_text().strip()
	if '무료' in delivery_cost:
		delivery_cost = 0
	else:
		delivery_cost = int(delivery_cost.replace(',', '').replace('원', ''))

	# 품절여부
	soldout = any(form.find_all('div', {'class': 'not_goods'}))

	# 옵션
	op_json_text = ''
	scripts = soup.find_all('script')
	for script in scripts:
		text = script.get_text()
		start = text.find('aCombinationOption')
		if start != -1:
			end = text.find('sOptionSortType')
			txt = text[start + 22:end]
			end2 = txt.find('],')
			op_json_text = txt[:end2] + ']'
	op_json = json.loads(op_json_text)
	options = []
	for op in op_json:
		options.append(dict(name=op['optionName1'], price=op['price']))

	result = dict(
		name=name,
		price=price,
		delivery_cost=delivery_cost,
		soldout=soldout,
		options=options
	)
	return result


def save_json(data):
	with open('output.json', 'w', encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)


def fetch_all():
	naver_data = [naver_store(fetch_url(url)) for url in naver_list]
	save_json(naver_data)
	return naver_data
