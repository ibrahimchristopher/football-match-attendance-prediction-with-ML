
#what data we actually want 
#team fanbase,ticket price,distance between two staduims, wheater conditions,special games(derby),position in table,timestamp,attendance,staduim capacity
#if fanbase data cant be obtained try using team value
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from data_converter import data_cleaner,json_to_csv

#requests the 38 week pages
def season_data_scrapper(season):
	season_data= {}
	season_years = season.split('_')
	for i in range(1,39):
		season_data[f'round {i}'] = {}
		url = f'https://www.worldfootball.net/schedule/eng-premier-league-20{season_years[0]}-20{season_years[1]}-spieltag/{i}/'
		r = requests.get(url)
		print(f'entered round {season} {i}')
		#gets links to weekly results
		html_contents = r.text
		html_soup = BeautifulSoup(html_contents, 'html.parser')
		td_class_hell= html_soup.find_all('td', attrs = {'class' : 'hell','align': 'center','nowrap':'nowrap'})
		td_class_dunkel= html_soup.find_all('td', attrs = {'class' : 'dunkel' ,'align': 'center','nowrap':'nowrap'})
		td_class = td_class_dunkel + td_class_hell
		#list to contain links to match results for each week
		match_result = []
		for td in td_class:
			if td.a:
				match_result.append(td.a['href'])
		#list to contain match details(teams playing and time they played)
		team_time = []

		y = 1
		for m in match_result:
			season_data[f'round {i}'][f'match {y}'] = {}
			
			url = 'https://www.worldfootball.net' + m
			r = requests.get(url)
			html_contents = r.text
			html_soup = BeautifulSoup(html_contents, 'html.parser')
			match= []

			#gets the teams that played and time they played
			th_list = html_soup.find_all('th', {'align' : 'center'})
			
			v = []
			td_all = html_soup.find_all('table', {})
			for t in (td_all[-1].find_all('tr')):
				v.append(t.text.strip())
			venue_attendance = v[:2]
			
			res = (html_soup.find('div', class_ = 'resultat')).text.strip()


			for th in th_list:
				match.append((th.text.strip()))
			match.append(res)
			team_time.append((match + venue_attendance))
			season_data[f'round {i}'][f'match {y}']['home'] = match[0]
			season_data[f'round {i}'][f'match {y}']['away'] = match[2]
			season_data[f'round {i}'][f'match {y}']['score'] = match[3]
			season_data[f'round {i}'][f'match {y}']['timestamp'] = match[1][:-6]
			season_data[f'round {i}'][f'match {y}']['venue'] = venue_attendance[0]
			season_data[f'round {i}'][f'match {y}']['attendance'] = venue_attendance[1]
			y += 1

	file = 'data.json'

	with open(file, 'w') as f:
		json.dump(season_data, f)
	
	data_cleaner(season)
	json_to_csv(season)

seasons = ['14_15','15_16','16_17','17_18','18_19']
for season in seasons:
	season_data_scrapper(season)