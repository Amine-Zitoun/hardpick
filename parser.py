import requests
import os
from bs4 import BeautifulSoup as bs


def search_megapc(comp,budget):
	if comp not in ['alimentation','barette-memoire',
	'boitier','carte-graphique','carte-mere','stockage',
	'processeur','refroidissement']:
		print("rip")
	else:
		url = "https://www.mega-pc.net/boutique/composants/"+comp
		res = requests.get(url)
		html = bs(res.text,'lxml')
		all_comp = [x.text for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
		prices = [x.text.split('\xa0')[0] for x in html.find_all('span',{'class': 'woocommerce-Price-amount amount'})]
		comp_prices = dict(zip(all_comp,prices))
		final_comp =[]
		for key,val in comp_prices.items():
			if int(val) <= budget:
				final_comp.append(key)
			else:
				pass
		print(final_comp)




def main():
	stores = ['sbstn','mega-pc']
	#comp = input("comp: ")
	#budget = input("budget: ")
	comp = "alimentation"
	budget= 500
	search_megapc(comp,budget)
main()