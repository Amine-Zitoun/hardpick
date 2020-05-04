import requests
import os
from bs4 import BeautifulSoup as bs
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

app = Flask(__name__)
api = Api(app)

class get_comp(Resource):
	def get(self,comp,budget):
		print(comp,budget)
		if comp not in ['alimentation','barette-memoire',
		'boitier','carte-graphique','carte-mere','stockage',
		'processeur','refroidissement']:
			print("rip")
		else:
			url = "https://www.mega-pc.net/boutique/composants/"+comp
			res = requests.get(url)
			html = bs(res.text,'lxml')
			#print(html)
			all_comp = [x.text for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
			prices = [x.text.split('\xa0')[0].replace(',','.') for x in html.find_all('span',{'class': 'woocommerce-Price-amount amount'})]
			comp_prices = dict(zip(all_comp,prices))
			
			final_comp =[]
			for key,val in comp_prices.items():

				if float(val) <= float(budget):
					final_comp.append(key)
				else:
					pass
			result = {'data': final_comp}
			return jsonify(result)
api.add_resource(get_comp, '/get_comp/<comp>/<budget>')

if __name__ == "__main__":
	app.run(port='5000')

