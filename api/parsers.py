
import requests
import os
from bs4 import BeautifulSoup as bs
from formattors import *




def process_prices(comp,all_comp,prices,budget,site,freqs,caps,typems):
	comp_prices = dict(zip(all_comp,prices))
	print(caps,typems,freqs,site)
	#print(comp_prices)
	final_comp =[]
	final_price =[]
	#print(comp_prices)


	final_frq =[]
	final_typem=[]
	final_cap=[]
	i = 0
	for key,val in comp_prices.items():
		if float(val) <= float(budget):
			try:
				final_frq.append(freqs[i])
				final_typem.append(typems[i])
				final_cap.append(caps[i])
			except:
				pass

			final_comp.append(key)
			final_price.append(float(val))
		else:
			pass
		i+=1


	dict_res=  dict(zip(final_comp,final_price))

	#print(dict_res)
	#print(len(final_frq))
	r = sorted(dict_res.items(), key=lambda item: item[1])
	#print(list(dict_res.keys()).index(r[-1][0]))
	#print(final_frq[list(dict_res.keys()).index(r[-1][0])])

	try:

		freq = final_frq[list(dict_res.keys()).index(r[-1][0])]
		cap  = final_cap[list(dict_res.keys()).index(r[-1][0])]
		typem = final_typem[list(dict_res.keys()).index(r[-1][0])]
	except:
		freq= 0
		cap = 0
		typem=0

	try:

		final_shit = {'site': site,
			'price': r[-1][1],
			 'prd': r[-1][0],
			"typem": typem,
			 "cap":cap,
			 'frq': freq}
	except IndexError:
		final_shit ={'site': site,'price': 0.0,'prd':'',"typem": 0,"cap":0,"frq": 0}
	return final_shit


def search_tunisia(comp,budget):
	url = "https://www.tunisianet.com.tn/"
	freqs=[]
	caps=[]
	typems=[]
	if comp == "gpu":
		comp = '410-carte-graphique'
	elif comp == "cpu":
		comp = "421-processeur"
	elif comp == "ram":
		comp = "409-barrette-memoire"

		caps,typems,freqs=ram_formattor(url+comp,"tunisia")
	res = requests.get(url+comp)
	html = bs(res.text,'lxml')
	#print(html)

	#s = html.find_all('h2',{'class': 'h3 product-title'})
	temp=[[y.text for y in x.findChildren('a',recursive=False)] for x in html.find_all('h2',{'class': 'h3 product-title'})]
	#print(s)
	all_comp = [x[0] for x in temp]
	#print(all_comp)
	#print(len(prices))
	all_prices = [float((y.text).replace('\xa0','').replace(',','').split('D')[0]) for y in html.find_all('span',{'class':'price'})]
	t = 0
	new_prices=[]
	while t <= len(all_prices)-1:
		new_prices.append(all_prices[t])
		t += 2
	#print(len(new_prices),new_prices)
	return process_prices(comp,all_comp,new_prices,budget,'tunisia',freqs,caps,typems)




def search_extreme(comp,budget):
	url = "https://extremegaming.tn/composants-accessoires/"
	res = requests.get(url)
	html = bs(res.text,'lxml')
	freqs=[]
	caps=[]
	typems=[]
	if comp == "gpu":
		div_name = "tab-carte-graphique"
	elif comp == "cpu":
		div_name  = "tab-cpu"
	elif comp == "ram":
		div_name = "tab-ram"
		caps,typems,freqs=ram_formattor(url,"extreme")
	products =[]
	prices = []
	s = html.find_all('div',{'id': div_name})
	for x in s:
		prd = x.find_all('h2')
		price = x.find_all('span',{'class': 'woocommerce-Price-amount amount'})
		for p,pr in zip(prd,price):
			products.append(p.text)
			prices.append(float(pr.text.split('.')[0].replace(',','')+"000"))
	print(dict(zip(products,prices)))
	return process_prices(comp,products,prices,budget,'extreme',freqs,caps,typems)



	#print(s.find('h2',{'class':'woocommerce-loop-product__title'}))
'''def search_wiki(comp,budget):
	if comp == "gpu":
		comp = "carte-graphique-131.html#"
		num_pages = 6
	if comp == "cpu":
		comp = "processeur-130.html"
		num_pages = 2
	if comp == "ram":
		comp = "barrette-memoire-133.html"
		num_pages = 1
	
	temp =[]
	all_comp=[]
	temp2=[]
	prices=[]
	url = "https://www.wiki.tn/c/"+comp+"/"
	res = requests.get(url)
	html = bs(res.text,'lxml')
	temp=[[y.text for y in x.findChildren('a',recursive=False)] for x in html.find_all('h4',{'class': 'name'})]
	all_comp = [x[0] for x in temp]

	temp2.append([[y.text for y in x.findChildren('span',recursive=False)]  for x  in html.find_all('div',{'class': 'content_price'})])

	prices.append([float(x[0].split('D')[0].replace(',','')) for x in temp2[0]])
	prices = prices[0]
	#print(prices)
	return process_prices(all_comp,all_prices,budget,'wiki')'''
def search_megapc(comp,budget):

	# Identify url from the comp type
	freqs=[]
	caps=[]
	typems=[]
	if comp == "gpu":
		comp = "carte-graphique"
		url = "https://www.mega-pc.net/boutique/composants/"+comp
	if comp == "cpu":
		comp = "processeur"
		url1 = "https://www.mega-pc.net/boutique/composants/"+comp
		url2 = "https://www.mega-pc.net/boutique/composants/"+comp+"/page/2/"
		res1 = requests.get(url1)
		html1 = bs(res1.text,'lxml')
		res2 = requests.get(url2)
		html2 = bs(res2.text,'lxml')
		#print(html)
		print("")
		for i in html2.find_all('span',{'class': 'price'}):
			if i.text.count("T") > 1:
				print(i.text.split(" ")[1].split('\xa0')[0].replace(',','')+"000")
			else:
				print(i.text.split('\xa0')[0].replace(',','')+"000")
			#print(i.text)
			print("\n\n")

		prices1=[]
		prices2=[]

		all_comp1 = [x.text for x in html1.find_all('h2',{'class': 'woocommerce-loop-product__title'})]


		for i in html1.find_all('span',{'class': 'price'}):
			if i.text.count("T") > 1:
				prices1.append(i.text.split(" ")[1].split('\xa0')[0].replace(',','')+"000")
			else:
				prices1.append(i.text.split('\xa0')[0].replace(',','')+"000")
			#print(i.text)
			#print("\n\n")


		#prices1 = [x.text.split('\xa0')[0].replace(',','')+"000" for x in html1.find_all('span',{'class': 'woocommerce-Price-amount amount'})]
		all_comp2 = [x.text for x in html2.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
		
		for i in html2.find_all('span',{'class': 'price'}):
			print(i.text.count("T"))
			if i.text.count("T") == 2:
				prices2.append(i.text.split(" ")[1].split('\xa0')[0].replace(',','')+"000")
			else:
				prices2.append(i.text.split('\xa0')[0].replace(',','')+"000")

		#prices2 = [x.text.split('\xa0')[0].replace(',','')+"000" for x in html2.find_all('span',{'class': 'woocommerce-Price-amount amount'})]
		
		#print()
		#print(all_comp2)
		#print(len(prices2),len(all_comp2))
		#print(dict(zip(all_comp2,prices2)))
		prices = prices1+prices2
		all_comp = all_comp1+all_comp2
		#print(len(prices),len(all_comp))
		#print(len(prices1),len(prices2))
		#print(len(all_comp1),len(all_comp2))
		#print(dict(zip(all_comp,prices)))
		return process_prices(comp,all_comp,prices,budget,'mega',freqs,caps,typems)

	if comp == "ram":
		comp = "barette-memoire"
		# Get the ram data from the ram_formattor function
		url = "https://www.mega-pc.net/boutique/composants/"+comp
		caps,typems,freqs=ram_formattor(url,"mega")
		print(caps,typems,freqs)
	
	# parse all products and according prices
	res = requests.get(url)
	html = bs(res.text,'lxml')
	#print(html)
	all_comp = [x.text for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
	prices = [x.text.split('\xa0')[0].replace(',','')+"000" for x in html.find_all('span',{'class': 'woocommerce-Price-amount amount'})]
	return process_prices(comp,all_comp,prices,budget,'mega',freqs,caps,typems)



#sdfsddfsdf
def search_sbs(comp,budget):

	freqs=[]
	typems=[]
	caps=[]

	# Identify url from the comp type

	if comp == "gpu":
		comp = "tunisie-cartes-graphiques"
		url = "http://www.sbsinformatique.com/"+comp
	elif comp == "cpu":
		comp ="tunisie-processeurs"
		url = "http://www.sbsinformatique.com/"+comp

	elif comp == "ram":
		comp = "tunisie-barettes-memoires"

		# Get the ram data from the ram_formattor function
		url = "http://www.sbsinformatique.com/"+comp
		caps,typems,freqs=ram_formattor(url,"sbs")

	# parse all products and according prices
	res = requests.get(url)
	html=bs(res.text,"lxml")
	all_comp = [x.text for x in html.find_all('b',{'class': 'VignBlue'})]
	status = [x.text.split('\xa0')[0] for x in html.find_all('span',{'class': 'DispoNew'})]
	print(status)
	prices = [x.text.split('D')[0].replace(',','')+"000" for x in html.find_all('b',{'class': 'bordeau14'})]
	comp_prices = dict(zip(all_comp,prices))

	# vars
	final_comp =[]
	final_price= []

	final_frq =[]
	final_typem=[]
	final_cap=[]
	i = 0

	# get all products with price lower then budget and update ram data
	for key,val in comp_prices.items():
		if val == "N.C 000":
			pass
		elif float(val) <= float(budget):
			if status[i] == "En stock":
				try:
					final_frq.append(freqs[i])
					final_typem.append(typems[i])
					final_cap.append(caps[i])
				except Exception as e:
					pass

				final_comp.append(key)
				final_price.append(float(val))
			else:
				pass
		i += 1

	# store in dict
	dict_res=  dict(zip(final_comp,final_price))
	# sort dict
	r = sorted(dict_res.items(), key=lambda item: item[1])
	try:

		freq = final_frq[list(dict_res.keys()).index(r[-1][0])]
		cap  = final_cap[list(dict_res.keys()).index(r[-1][0])]
		typem = final_typem[list(dict_res.keys()).index(r[-1][0])]
	except:
		freq= 0
		cap = 0
		typem=0

	try:

		final_shit = {
			'site': 'sbs',
			'price': r[-1][1],
			 'prd': r[-1][0],
			"typem": typem,
			 "cap":cap,
			 'frq': freq}
	except IndexError:
		final_shit ={'site': 'sbs','price': 0.0,'prd':'',"typem": 0,"cap":0,"frq": 0 }
	return final_shit

