import requests
import os
from bs4 import BeautifulSoup as bs
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

app = Flask(__name__)
app.debug = True
api = Api(app)
'''
http://www.sbsinformatique.com/
https://www.wiki.tn/
https://www.scoop.com.tn/'''

def cpu_formattor(cpu):
	res_cpu = ''
	#print("BEFORE FORMATTING: ",cpu)
	if cpu.lower().startswith('processeur'):
		new_cpu = cpu[11:]
	else:
		new_cpu = cpu
	if new_cpu.lower().startswith('amd'):
		res_cpu = ' '.join(new_cpu.split(' ')[:4])
	if new_cpu.lower().startswith('intel'):
		res_cpu = ' '.join(new_cpu.split(' ')[:3])
	#print("AFTER FORMATTING: ",res_cpu)
	return res_cpu.lower()

def gpu_val(gpu):
	res_gpu = ''
	arr = gpu.split(' ')
	if 'G' in arr[-1]:
		vl = arr[-1].split('G')[0]
	else:
		if 'G' in arr[-2]:
			vl = arr[-2].split('G')[0]
		else:
			if 'G' in arr[-3]:
				vl = arr[-3].split('G')[0]

	return int(vl)

def benchmark(c1,c2,comp):
	print(c1,c2)
	if comp == "gpu":
		vl1 = gpu_val(c1)
		vl2 = gpu_val(c2)
		if vl1 >= vl2:
			return c1
		else:
			return c2
	elif comp == "cpu":
		url = "https://www.cpubenchmark.net/high_end_cpus.html"
		#print(url)
		c1 = cpu_formattor(c1)
		c2 = cpu_formattor(c2)
		print(c1,c2)
		res = requests.get(url)
		html = bs(res.text,'lxml')
		#print(html)
		parts = [cpu_formattor(x.text).lower() for x in html.find_all('span',{'class': 'prdname'})]
		points = [float(x.text.replace(',','.')) for x in html.find_all('span',{'class': 'mark-neww'})]
		final_res = dict(zip(parts,points))
		
		if c1.lower() in final_res.keys():
			c1_vl = final_res[c1]
		else:
			print(c1+"not found")
			c1_vl = 0

		if c2.lower() in final_res.keys():
			c2_vl = final_res[c2]
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
	final_shit = {'site': 'mega-pc','price': r[-1][1], 'prd': r[-1][0]}
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
	final_shit ={'site': 'sbs','price': r[-1][1], 'prd': r[-1][0]}
	return final_shit


class get_comp(Resource):
	def get(self,comp,budget):
		print(comp,budget)
		l1 = search_megapc(comp,budget)
		prd1= l1['prd'].encode('ascii', 'ignore').decode('unicode_escape')
		print(l1)
		l2 = search_sbs(comp,budget)
		prd2 =l2['prd'].encode('ascii', 'ignore').decode('unicode_escape')
		win = benchmark(prd1,prd2,comp)
		result = {'data': [l1,l2,win]}
		return jsonify(result)


api.add_resource(get_comp, '/get_comp/<comp>/<budget>')

if __name__ == "__main__":
	#print("INTEL® CORE™ I7-7800X".encode('ascii', 'ignore').decode('unicode_escape'))
	#benchmark("AMD Ryzen 7 3700X".encode('ascii', 'ignore').decode('unicode_escape'),"INTEL® CORE™ I7-7800X".encode('ascii', 'ignore').decode('unicode_escape'),'cpu')
	app.run(port='5000')

