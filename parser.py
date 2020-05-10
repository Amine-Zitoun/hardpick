
import requests
import os
from bs4 import BeautifulSoup as bs
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

# yo
# zitoun zabour
app = Flask(__name__)
app.debug = True
api = Api(app)
'''
http://www.sbsinformatique.com/
https://www.wiki.tn/
https://www.scoop.com.tn/'''



def search_intense(key,l):
	print("zbi?")
	for i in l:
		#print("CHECKING "+key+" with "+i)
		print("checking ",i,"with ",key)
		if key in i:
			#print("CHECKING "+key+" with "+i)
			print('FOUND MATCH')
			return i
		else:
			pass
	return "not found"





def ram_formattor(url,site):
	if site == "sbs":
		s = requests.get(url)
		html = bs(s.text,'lxml')
		desc = html.find_all('div',{'class': 'descriptonProd'})
		#print(len(desc))
		#print("=======================================")
		caps = []
		typems = []
		freqs= []

		for t in desc:

			for f in t.findChildren('p',recursive=False):
				
				#print(f.text.split("Fréquence"))
				if len(f.text.split('mémoire')) > 1:
					
					#print(f.text.split('mémoire')[1].split(' ')[2].split('\n')[0])
					typems.append(f.text.split('mémoire')[1].split(' ')[2].split('\n')[0].split('\r')[0])
				if len(f.text.split('Capacité')) > 1:
					
					#print(f.text.split('Capacité')[1].split(' ')[2].split('\n')[0])
					caps.append(int(f.text.split('Capacité')[1].split(' ')[2].split('\n')[0]))
				if len(f.text.split('Fréquence')) > 1:
					freqs.append(int(f.text.split('Fréquence')[1].split(' ')[2].split('\n')[0]))
					#print(f.text.split('Fréquence')[1].split(' ')[2].split('\n')[0])


		return caps,typems,freqs
	elif site == "mega":
		# parse all products and according prices
		res = requests.get(url)
		html = bs(res.text,'lxml')
		#print(html)
		all_comp = [x.text for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
		caps = []
		typems = []
		freqs= []
		for s in all_comp:
			
			print("testing on "+s)
			count = 0

			capd=None
			freqd=None
			typemd=None

			if s.split(' ')[0].lower() == "corsair" and s.split(' ')[3][0] != "8":
				if s.split(' ')[2].lower() == "lpx":
					capd=1
					typemd=6
					freqd=7
				elif s.split(' ')[2].lower() == "rgb":
					if s.split(' ')[4][0] == "3":
						caps.append(32)
						freqs.append(3000)
						typems.append("DDR4")
						pass
					else:
						capd=1
						typemd=5
						freqd=6
			elif s.lower().startswith('gigabyte aorus'):
				capd=2
				typemd=1
				freqd=6
			elif s.lower().startswith('patriot'):
				capd=1
				typemd=5
				freqd=6
			elif s.lower().startswith('g.skill'):
				capd=1
				typemd=5
				freqd=6
			else:
				capd=1
				typemd=4
				freqd=5



			#print(s.lower().startswith('patriot'))

			print(capd,typemd,freqd)
			cap=None
			typem=None
			frq=None
			#print(typemd)
			for i in s:
				if i.isdigit():
					count += 1
					if count == capd:
						if s[s.index(i)+1] == "G":
							caps.append(int(i))
						elif s[s.index(i)+1] != "G":
							caps.append(int(i+''+s[s.index(i)+1]))
						#print("IMPORTANT ON "+i)
					elif count == typemd:
						typems.append("DDR"+i)
					elif count == freqd:
						print(count)
						print(s.index(i))
						print(i+s[s.index(i)+1]+s[s.index(i)+2]+s[s.index(i)+3])
						freqs.append(int(i+s[s.index(i)+1]+s[s.index(i)+2]+s[s.index(i)+3]))
		print( caps,typems,freqs)
		return caps,typems,freqs
	if site == "extreme":
		res = requests.get(url)
		caps = []
		typems = []
		freqs= []
		html = bs(res.text,'lxml')
		#print(html)
		#all_comp = [x.text.encode('ascii', 'ignore').decode('unicode_escape') for x in html.find_all('h2',{'class': 'woocommerce-loop-product__title'})]
		products=[]
		s = html.find_all('div',{'id': "tab-ram"})
		for x in s:
			prd = x.find_all('h2')
		#price = x.find_all('span',{'class': 'woocommerce-Price-amount amount'})
			for p in prd:
				products.append(p.text.encode('ascii', 'ignore').decode('unicode_escape'))




		for i in products:
			print("vengeance" == i.lower().split(' ')[0],i.lower().split(' ')[0])
			if "pny" in i.lower() and "8" in i.lower():
				caps.append(8)
				typems.append("DDR4")
				freqs.append(2666)

			elif i.lower().split(' ')[0] == "vengeance":
				if "3000Mhz" in i.lower():
					caps.append(16)
					freqs.append(3000)
					typems.append("DDR4")
				else:
					caps.append(16)
					freqs.append(3200)
					typems.append("DDR4")
			elif i.startswith("16"):
				caps.append(16)
				freqs.append(2666)
				typems.append("DDR4")
			else:
				caps.append(8)
				freqs.append(3000)
				typems.append("DDR4")

		print( caps,typems,freqs)
		return caps,typems,freqs

def cpu_formattor(cpu,site):
	word= cpu.split(' ')
	if site == "sbs" or site == "mega":
		if cpu[0].lower() == "p":
			res_word=word[1:]
		else:
			res_word = word

		if res_word[0].lower() == "intel":
			key = res_word[0] +' '+ res_word[1] +' '+ res_word[2] 
		elif res_word[0].lower() == "amd":
			key = res_word[0] + ' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
		return key
	if site == "extreme":
		res_word = word
		if res_word[0].lower() == "amd":
			key = cpu.lower()
		if res_word[0].lower() == "cpu":
			key = res_word[1]+' '+res_word[2]+' '+res_word[3]
		if res_word[0].lower() == "intel":
			if res_word[1].lower() == "i9":
				key = res_word[1]+'-'+res_word[2]
			else:
				key = cpu.lower().split('-')[0]+cpu.lower().split('-')[1]+cpu.lower().split('-')[2]
		if res_word[0].lower().startswith('pent'):
			key = cpu.lower()
		if res_word[0].lower().startswith('ry'):
			key = "amd"+' '+cpu.lower()
		if res_word[0].lower().startswith('pro'):
			key = ' '.join(res_word[1:])
		return key



	#return res_cpu.lower()

def gpu_val(gpu,site):
	#print("\n\n\n\n"+gpu+"\n\n\n")
	res_gpu = ''
	arr = gpu.split(' ')
	if site == "sbs":
		word = gpu.split(' ')
		#for i in word:
		res_word = word[2:]
		if res_word[0] == "Palit":
			if res_word[1] == "GeForce":
				if res_word[2] == "GT":
					key = res_word[2]+' '+res_word[3]
				elif res_word[2] == "RTX":
					key = res_word[2]+' '+res_word[3]+' '+res_word[4]
			elif res_word[1] == "RTX":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			elif  res_word[1] == "GT":
				key = res_word[1]+' '+res_word[2]
			elif res_word[1] == "GTX":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			return key
		elif res_word[0] == "MSI":
			if res_word[1] == "GeForce":
				if res_word[2] == "GT":
					key = res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key = res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
			elif res_word[1] == "GTX":
				key = res_word[1]+' '+res_word[2]+' '
				if res_word[3] == "SUPER":
					key += res_word[3]
			elif res_word[1] == "Radeon":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			elif res_word[1] == "RTX":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			return key
		elif res_word[0] == "ASUS":
			if res_word[1].lower() == "rog":
				if res_word[2].lower() == "strix":
					if res_word[3].lower()[:2] == "RX":
						key = res_word[3]
					else:
						key = res_word[3] + ' '+res_word[4] + ' '+res_word[5]
			elif res_word[1].lower() == "tuf":
				if c:
					key  = res_word[2] + ' '+res_word[3]+' '+res_word[4]
				elif res_word[2].lower() == "3-":
					key = res_word[3]
			elif res_word[1].lower() == "gtx":
				key = res_word[1]+' '+res_word[2]+' '+res_word[3]
			return key
	if site == "mega":
		word = gpu.split(' ')
		res_word = word[1:]

		if res_word[3].lower() == "super":
			key = res_word[0]+' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
		else:
			key = res_word[0]+' '+res_word[1]+' '+res_word[2]
		return key.lower()
	if site == "extreme":
		res_word = gpu.split(' ')
		if res_word[0].lower() == "geforce":
			if res_word[1].lower() == "rtx":
				if res_word[3].lower() == "super" or res_word[3].lower() == "ti":
					key = res_word[0]+' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key = res_word[0]+' '+res_word[1]+' '+res_word[2]
			elif res_word[1].lower() == "gt":
				key = res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "gtx":
			key = res_word[0]+' '+res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "gtx1660":
			key = "gtx 1660"
		if res_word[0].lower() == "pny":
			if res_word[1].lower() == "1660":
				key = "gtx 1660 super"
			else:
				key = res_word[0]+' '+res_word[1]+' '+res_word[2]+' '+res_word[3]
		if res_word[0].lower() == "msi":
			key = res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "asus":
			key = res_word[2]
		return key
	if site == "tunisia":
		word =gpu.split(' ')
		res_word =word[2:]
		if res_word[0].lower() == "palit":
			if res_word[1].lower() == "geforce":
				if res_word[2].lower() == "gt":
					key = res_word[2] + ' '+res_word[3]
				elif res_word[2].lower() == "gtx":
					if res_word[4].lower() in ['ti','super']:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
					else:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key =res_word[1]+' '+res_word[2]
			elif res_word[1].lower() == "gtx":
				if res_word[3].lower() in ['ti','super']:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]
					else:
						key = res_word[1]+' '+res_word[2]
		if res_word[0].lower() == "gigabyte":
			if res_word[1].lower() == "geforce":
				if res_word[2].lower() == "gtx":
					if res_word[4].lower() in ['ti','super']:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]+' '+res_word[4]
					else:
						key = res_word[1]+' '+res_word[2]+' '+res_word[3]
				else:
					key = res_word[1]+' '+res_word[2]
			if res_word[1].lower() == "gtx": 
				if res_word[3].lower() in ['ti','super']:
					key = res_word[1]+' '+res_word[2]+' '+res_word[3] 
				else:
					key = res_word[1]+' '+res_word[2]
		if res_word[1].lower() == "msi":
			if res_word[2].lower() == "geforce":
				if res_word[5].lower() in ['ti','super']:
					key = res_word[2]+' '+res_word[3]+' '+res_word[4]+' '+res_word[5]
				else:
					key =res_word[2]+' '+res_word[3]+' '+res_word[4]
			if res_word[2].lower() == "radeon":
				key =res_word[2]+' '+res_word[3]+' '+res_word[4]
			if res_word[2].lower() == "gtx":
				key =res_word[2]+' '+res_word[3]+' '+res_word[4]
		if res_word[1].lower() == "asus":
			if res_word[2].lower() == "geforce":
				key =res_word[2]+' '+res_word[3]+' '+res_word[4]+' '+res_word[5]
			else:
				key ="radeon rx 5700 xt"
		return key


			

		

	#return int(vl)

def benchmark(c1,c2,comp):
	print(c1,c2)
	if comp == "gpu":
		# GET ALL THE PARTS FROM THE LEADERBOARD

		url = "https://www.videocardbenchmark.net/high_end_gpus.html"
		res = requests.get(url)
		html = bs(res.text,'lxml')
		parts = [(x.text).lower() for x in html.find_all('span',{'class': 'prdname'})]
		points = [float(x.text.replace(',','.')) for x in html.find_all('span',{'class': 'mark-neww'})]

		final_res = dict(zip(parts,points))

		# FORMATS THE NAME OF THE PRODUCT 
		print("[*] FOUND ON SITE: "+c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'))

		key1 = gpu_val(c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c1['site'])

		print("[*] TURNED IT INTO: "+key1)
		#print(parts)

		# searches in the learderboard

		res1= search_intense(key1.lower(),parts)
		print("[*] CHCKED ON DB AND FOUND: "+res1)

		# gets value
		if res1 != "not found":	
			vl1=final_res[res1]
		else:
			vl1 = 0
		#same process for 2
		key2 = gpu_val(c2['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c2['site'])
		print("[*] TURNED IT INTO: "+key2)
		print(parts)
		res2= search_intense(key2.lower(),parts)
		print("[*] CHCKED ON DB AND FOUND: "+res2)
		if res2 != "not found":	
			vl2=final_res[res2]
		else:
			vl2 = 0

		#compares values

		if vl1 >= vl2:
			return c1
		else:
			return c2


	elif comp == "cpu":
		url = "https://www.cpubenchmark.net/high_end_cpus.html"
		#print(url)
		# GET ALL THE PARTS FROM THE LEADERBOARD


		res = requests.get(url)
		html = bs(res.text,'lxml')
		parts = [(x.text).lower() for x in html.find_all('span',{'class': 'prdname'})]
		points = [float(x.text.replace(',','.')) for x in html.find_all('span',{'class': 'mark-neww'})]
		final_res = dict(zip(parts,points))


		# FORMATS THE NAME OF THE PRODUCT 
		key1 = cpu_formattor(c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c1['site'])
		print("[*]  FOUND ON SITE: "+c1['prd'].encode('ascii', 'ignore').decode('unicode_escape'))
		print("[*] TURNED IT INTO: "+key1)
		res1= search_intense(key1.lower(),parts)
		print("[*] CHCKED ON DB AND FOUND: "+res1)
		# gets value
		vl1=final_res[res1]

		# same process
		key2 = cpu_formattor(c2['prd'].encode('ascii', 'ignore').decode('unicode_escape'),c2['site'])
		print("[*]  FOUND ON SITE: "+c2['prd'].encode('ascii', 'ignore').decode('unicode_escape'))
		print("[*] TURNED IT INTO: "+key2)
		print(parts)
		res2= search_intense(key2.lower(),parts)
		print("[*] CHCKED ON DB AND FOUND: "+res2)
		vl2=final_res[res2]

		# compares vls
		if vl1 >= vl2:
			return c1
		else:
			return c2

		
	
	elif comp == "ram":
		# gets ram data from both

		frq1 = int(c1['frq'])
		cap1 = int(c1['cap'])
		typem1 = c1['typem']

		frq2 = int(c2['frq'])
		cap2 = int(c2['cap'])
		typem2 = c2['typem']

		pt1=0
		pt2=0
		# compares data

		if frq1 > frq2:
			pt1 += 1
		elif frq1 < frq2:
			pt2 += 1
		else:
			pass

		if cap1 > cap2:
			pt1 += 1
		elif cap1 < cap2:
			pt2 += 1
		else:
			pass

		if int(typem1[-1]) > int(typem2[-1]):
			pt1 += 1
		elif int(typem1[-1]) < int(typem2[-1]):
			pt2 += 1
		else:
			pass

		# compares vls
		if pt1 >= pt2:
			return c1
		else:
			return c2


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
	if comp == "gpu":
		comp = '410-carte-graphique'
	elif comp == "cpu":
		comp = "421-processeur"
	elif comp == "ram":
		comp = "409-barrette-memoire"

		caps,typems,freqs=ram_formattor(url+comp,"tunisia")
	res = requests.get(url+comp)
	html = bs(res.text,'lxml')
	print(html)

	#s = html.find_all('h2',{'class': 'h3 product-title'})
	temp=[[y.text for y in x.findChildren('a',recursive=False)] for x in html.find_all('h2',{'class': 'h3 product-title'})]
	#print(s)
	all_comp = [x[0] for x in temp]
	print(all_comp)
	all_prices = [float((y.text).replace('\xa0','').replace(',','').split('D')[0]) for y in html.find_all('span',{'class':'price'})]
	return process_prices(all_comp,all_prices,budget,'tunisia',freqs,caps,typems)




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


@app.route('/api/',methods=['GET'])
def res():
	comp= request.args.get('comp',None)
	budget = request.args.get('budget',None)
	print(comp,budget)
	# Searches for mega pc 
	mega = search_megapc(comp,budget)
	mega_prd= mega['prd'].encode('ascii', 'ignore').decode('unicode_escape')

	# Searches for sbs 
	sbs = search_sbs(comp,budget)
	sbs_prd =sbs['prd'].encode('ascii', 'ignore').decode('unicode_escape')
		
	# Search extreme
	extrme = search_extreme(comp,budget)
	extrme_prd =extrme['prd'].encode('ascii', 'ignore').decode('unicode_escape')
	
	# Search tunisianet
	#tn = search_tunisia(comp,budget)
	#tn_prd =tn['prd'].encode('ascii', 'ignore').decode('unicode_escape')

	#print(mega_prd)
	# benchmark all products
	win1 = benchmark(sbs,mega,comp)
	win2 = benchmark(win1,extrme,comp)
	result = {'data': [mega,sbs,extrme],'win': win2}
	return jsonify(result)
#api.add_resource(get_comp, '/get_comp/<comp>/<budget>')
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"
if __name__ == "__main__":
	#print("INTEL® CORE™ I7-7800X".encode('ascii', 'ignore').decode('unicode_escape'))
	#benchmark("AMD Ryzen 7 3700X".encode('ascii', 'ignore').decode('unicode_escape'),"INTEL® CORE™ I7-7800X".encode('ascii', 'ignore').decode('unicode_escape'),'cpu')
	#for i in range(149000,500000000000000000000):
	#ram_formattor("zz","http://www.sbsinformatique.com/tunisie-barettes-memoires","sbs")
	#print(search_sbs("ram",500000))
	#benchmark(search_sbs('cpu',100000000000000),"ss","ss","cpu")
	print(search_tunisia('gpu',500000000))
	#app.run(port='5000')
	#print(gpu_val("ASUS GeForce GTX 1660 SUPER TUF GAMING 6GB OC","mega"))