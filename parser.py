import requests
import os
from bs4 import BeautifulSoup as bs
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

app = Flask(__name__)
api = Api(app)
'''
http://www.sbsinformatique.com/
https://www.wiki.tn/
https://www.scoop.com.tn/'''

def cpu_formattor(cpu):
	if cpu.startswith('Processeur'):
		new_cpu = cpu[11:]
	else:
		new_cpu = cpu
	if new_cpu.startswith('AMD'):
		res_cpu = ' '.join(new_cpu.split(' ')[:4])
	if new_cpu.startswith('Intel'):
		res_cpu = ' '.join(new_cpu.split(' ')[:3])
	return res_cpu

def benchmark(c1,c2,comp):
	print(c1,c2)
	if comp == "gpu":
		url = "https://www.videocardbenchmark.net/gpu_value.html"
		res = requests.get(url)
		html = bs(res.text,'lxml')
		#print(html)
		parts = [x.text.lower() for x in html.find_all('span',{'class': 'prdname'})]
		points = [float(x.text.replace(',','.')) for x in html.find_all('span',{'class': 'mark-neww'})]
		final_res = dict(zip(parts,points))
		print(c1.lower() in [x.lower() for x in final_res.keys()])
		if c1.lower() in final_res.keys():
			c1_vl = final_res[c1.lower()]
		else:
			c1_vl = 0

		if c2.lower() in final_res.keys():
			c2_vl = final_res[c2.lower()]
		else:
			c2_vl = 0
		if c2_vl >= c1_vl:
			return c2
		else:
			return c1
	elif comp == "cpu":
		url = "https://www.cpubenchmark.net/cpu_value_available.html"
		#print(url)
		c1 = cpu_formattor(c1)
		c2 = cpu_formattor(c2)
		res = requests.get(url)
		html = bs(res.text,'lxml')
		#print(html)
		parts = [x.text.lower() for x in html.find_all('span',{'class': 'prdname'})]
		points = [float(x.text.replace(',','.')) for x in html.find_all('span',{'class': 'mark-neww'})]
		final_res = dict(zip(parts,points))
		
		if c1.lower() in final_res.keys():
			c1_vl = final_res[c1.lower()]
		else:
			print(c1+"not found")
			c1_vl = 0

		if c2.lower() in final_res.keys():
			c2_vl = final_res[c2.lower()]
		else:
			print(c2+"not found")
			c2_vl = 0
		if c1_vl >= c2_vl:
			return c1
		else:
			return c2
	elif comp == "ram":
		url ="https://ram.userbenchmark.com"
	


def search_megapc(comp,budget):
	if comp == "gpu":
		comp = "carte-graphique"
	if comp == "cpu":
		comp = "processeur"
	if comp == "ram":
		comp = "barette-memoire"
	url = "https://www.mega-pc.net/boutique/composants/"+comp
	res = requests.get(url)
	html = bs(res.text,'lxml')
	#print(html)
	all_comp = [x.text for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
	prices = [x.text.split('\xa0')[0].replace(',','') for x in html.find_all('span',{'class': 'woocommerce-Price-amount amount'})]
	comp_prices = dict(zip(all_comp,prices))
	
	final_comp =[]
	final_price =[]
	for key,val in comp_prices.items():
		if float(val) <= float(budget):
			final_comp.append(key)
			final_price.append(float(val))
		else:
			pass
	dict_res=  dict(zip(final_comp,final_price))

	r = sorted(dict_res.items(), key=lambda item: item[1])
	print(r)
	final_shit = r[-1][0]
	return final_shit


def search_sbs(comp,budget):
	if comp == "gpu":
		comp = "tunisie-cartes-graphiques"
	elif comp == "cpu":
		comp ="tunisie-processeurs"
	elif comp == "ram":
		comp = "tunisie-barettes-memoires"
	url = "http://www.sbsinformatique.com/"+comp
	res = requests.get(url)
	html=bs(res.text,"lxml")
	all_comp = [x.text for x in html.find_all('b',{'class': 'VignBlue'})]
	prices = [x.text.split('D')[0].replace(',','') for x in html.find_all('b',{'class': 'bordeau14'})]
	comp_prices = dict(zip(all_comp,prices))
	final_comp =[]
	final_price= []
	for key,val in comp_prices.items():

			if float(val) <= float(budget):
				final_comp.append(key)
				final_price.append(float(val))
			else:
				pass
	dict_res=  dict(zip(final_comp,final_price))
	r = sorted(dict_res.items(), key=lambda item: item[1])
	print(r)
	final_shit = r[-1][0]
	return final_shit


class get_comp(Resource):
	def get(self,comp,budget):
		print(comp,budget)
		l1 = search_megapc(comp,budget)
		print(l1)
		l2 = search_sbs(comp,budget)
		print(l2)
		win = benchmark(l1,l2,comp)
		result = {'data': win}
		return jsonify(result)


api.add_resource(get_comp, '/get_comp/<comp>/<budget>')

if __name__ == "__main__":
	#print("INTEL® CORE™ I7-7800X".encode('ascii', 'ignore').decode('unicode_escape'))
	#benchmark("AMD Ryzen 7 3700X".encode('ascii', 'ignore').decode('unicode_escape'),'s','cpu')
	app.run(port='5000')

