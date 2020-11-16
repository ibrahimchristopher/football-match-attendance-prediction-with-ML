import json
import pandas as pd
def data_cleaner(season):
	"""
	this function converts data scraped from target website
	into a more structured, usable and standard form
	"""
#accessing unstructured json file 	
	file = 'data.json'
	with open(file) as f:
		dict_data = json.load(f)
#data will be a list of a list of a list
#[[round 1 matches and their details....],[[match 1 and details],[match 2 and details]], []]
#creating final list(empty) to contain data
	current_season = []
	#looping through dictionaries in data.json and appending match details to final list
	for i in range(1,39):
		r = []
		for j in range (1,11):
			m = []
			m.append(f'r{i}')
			m.append(f'm{j}')
			m.append(dict_data[f'round {i}'][f'match {j}']['timestamp'][:-5])
			m.append(dict_data[f'round {i}'][f'match {j}']['timestamp'][-5:])
			m.append(dict_data[f'round {i}'][f'match {j}']['home'])
			m.append(dict_data[f'round {i}'][f'match {j}']['away'])
			m.append(dict_data[f'round {i}'][f'match {j}']['score'])
			m.append(dict_data[f'round {i}'][f'match {j}']['venue'])
			m.append(dict_data[f'round {i}'][f'match {j}']['attendance'])
			r.append(m)
		current_season.append(r)
			

	#creating final json file to store data structure(final list)
	season_years = season.split('_')
	file = f'season_{season_years[0]}_{season_years[1]}.json'

	with open(file, 'w') as f:
		json.dump(current_season, f)	

def json_to_csv(season):
	season_years = season.split('_')
	file = f'season_{season_years[0]}_{season_years[1]}.json'
	season_dict = {'round': [],'match':[],'date':[],'time':[],'home':[],'away':[],'score':[],'venue':[],'attendance':[]}
	with open(file) as f:
		list_of_rounds = json.load(f)
	for matches in list_of_rounds:
		for match in matches:
			season_dict['round'].append(match[0])
			season_dict['match'].append(match[1])
			season_dict['date'].append(match[2])
			season_dict['time'].append(match[3])
			season_dict['home'].append(match[4])
			season_dict['away'].append(match[5])
			season_dict['score'].append(match[6])
			season_dict['venue'].append(match[7])
			season_dict['attendance'].append(match[8])
	df = pd.DataFrame(season_dict)
	df.to_csv(f'season_{season}.csv',)	
