from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
import plotly.express as px
import pandas as pd
from plotly.offline import plot
import matplotlib.pyplot as plt

from requests.models import default_hooks

site = requests.get("https://www.otodom.pl/wynajem/mieszkanie/?nrAdsPerPage=72")
soup = BeautifulSoup(site.content, 'html.parser')

def getOfferTitle():
	titles = [i.get_text() for i in soup.select('span.offer-item-title')]
	return titles

def getPlace():
	places = [i.get_text().replace('Mieszkanie na wynajem: ', '').split(', ') for i in soup.select('p.text-nowrap')]
	return places

def getCities(places):
	cities = [i[0] for i in places]
	return cities

def getDistricts(places):
	tmp = [i[1:] for i in places]
	districts = [', '.join(i) for i in tmp]
	return districts

def getPrices():
	price = [float(i.get_text().replace(' ', '').replace('\n', '').replace('zł/mc', '').replace(',', '.')) for i in soup.select('li.offer-item-price')]
	return price

def getYardage():
	yardage = [float(i.get_text().replace(' m²', '').replace(',', '.')) for i in soup.select('li.offer-item-area')]
	return yardage

def getRooms():
	rooms = [int(i.get_text()[:1]) for i in soup.select('li.offer-item-rooms')]
	return rooms

def getData():
	data = pd.DataFrame()
	places = getPlace()
	data['Tytuł'] = getOfferTitle()
	data['Miasto'] = getCities(places)
	data['Dzielnica'] = getDistricts(places)
	data['Cena'] = getPrices()
	data['Metraż'] = getYardage()
	data['Pokoje'] = getRooms()
	return data

def getIntroTable():
	offers = data['Tytuł'].count()
	most_freq = data['Miasto'].value_counts().idxmax()
	avg_price = data['Cena'].mean()
	avg_yardage = data['Metraż'].mean()
	avg_rooms = data['Pokoje'].mean()
	most_dist = data['Dzielnica'].value_counts().idxmax()

	price_for_m = data['Cena'].sum() / data['Metraż'].sum()


	table = f'''<table class="table table-bordered table-striped">
	<thead><tr><th scope="col">Dane</th><th scope="col">#</th></tr></thead>
	<tr><td>Ilość zescrapowanych ofert</td><td>{data['Tytuł'].count()}</td></tr>
	<tr><td>Najczęściej występujące miasto</td><td>{data['Miasto'].value_counts().idxmax()}</td></tr>
	<tr><td>Najczęściej występująca dzielnica</td><td>{data['Miasto'].value_counts().idxmax()}, {data['Dzielnica'].value_counts().idxmax()}</td></tr>
	<tr><td>Najtańsza oferta</td><td>{data['Cena'].min()} zł/mc</td></tr>
	<tr><td>Najdroższa oferta</td><td>{data['Cena'].max()} zł/mc</td></tr>
	<tr><td>Średnia cena mieszkania</td><td>{round(data['Cena'].mean(), 2)} zł/mc</td></tr>
	<tr><td>Średnia cena za m²</td><td>{round(data['Cena'].sum() / data['Metraż'].sum(), 2)} zł</td></tr>
	<tr><td>Średni metraż mieszkania</td><td>{round(data['Metraż'].mean(), 2)} m²</td></tr>
	<tr><td>Średnia ilość pokoi</td><td>{int(data['Pokoje'].mean())}</td></tr>
	</table>'''
	return table

def drawCityDiagram():
	df = pd.DataFrame(data['Miasto'].value_counts())
	df.columns = ['Ilosc']
	df.index.name = 'Miasto'
	fig = px.pie(df, values="Ilosc", names=df.index, height=600)
	fig.update_traces(textposition='inside', textinfo='percent+label')
	plot_div = plot(fig, output_type='div')
	return plot_div

def getYards():
	D = dict({
		'0-20': 0,
		'20-30': 0,
		'30-40': 0,
		'40-50': 0,
		'50-60': 0,
		'60-70': 0,
		'70+': 0,
	})
	for i in data['Metraż']:
		if i >= 0 and i < 20:
			D['0-20'] += 1
		elif i >= 20 and i < 30:
			D['20-30'] += 1
		elif i >= 30 and i < 40:
			D['30-40'] += 1
		elif i >= 40 and i < 50:
			D['40-50'] += 1
		elif i >= 50 and i < 60:
			D['50-60'] += 1
		elif i >= 60 and i < 70:
			D['60-70'] += 1
		elif i >= 70:
			D['70+'] += 1
	return D


def drawYardageDiagram():	
	D = getYards()
	df = pd.DataFrame.from_dict(D, orient='index')
	df.index.name = 'Metraż mieszkania w m²'
	df.columns=['Ilość ofert']
	fig = px.line(df, x=df.index, y='Ilość ofert')
	fig.update_layout(showlegend=False)
	plot_div = plot(fig, output_type='div')
	return plot_div

def drawRoomDiagram():
	df = pd.DataFrame(data['Pokoje'].value_counts())
	df.columns = ['Ilość ofert']
	df.index.name = "Ilość pokoi w mieszkaniu"
	fig = px.bar(df, x=df.index, y='Ilość ofert', text='Ilość ofert', color=['red', 'green', 'blue', 'cyan'])
	fig.update_layout(showlegend=False)
	plot_div = plot(fig, output_type='div')
	return plot_div

data = getData()