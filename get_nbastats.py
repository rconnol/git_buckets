import string
import pandas as pd
import numpy as np
from datetime import datetime
from scrapinghub import ScrapinghubClient

def connect_to_client(api_key):

	client = ScrapinghubClient(api_key)

	return client

def get_spider(project, name):

	spider = project.spiders.get(name)

	return spider

def get_newest_job(project, spider):

	for job in spider.jobs.iter():

		return project.jobs.get(job['key'])

def get_data(api_key, project_num, project_name, to_csv=True):

	"""

	Newest web scrape from ScrapingHub Project

	Input - scraping hub api, proj. num, proj. name
	Output - Return: pandas DataFrame, save to_csv if True
	
	"""

	#data will be appended as dictionary to list
	data_stream = []

	#get newest job from client
	client = connect_to_client(api_key)
	project = client.get_project(project_num)
	spider = get_spider(project, project_name)
	job = get_newest_job(project=project, spider=spider)

	#filename
	translator = str.maketrans('', '', string.punctuation)
	date_ = str(datetime.now().date()).translate(translator)
	filename = 'bballref_player' + date_ + '.csv'
	
	#iterate through data stream
	for item in job.items.iter():

		data_stream.append(item)

	#create pandas DataFrame
	df = pd.DataFrame(data_stream)
	df = df.applymap(lambda x: x[0] if pd.notnull(x) else np.nan)
	df = df.convert_objects(convert_numeric=True)
	df = df.drop('_type', axis=1) #this is state, TRY TO REMOVE
	
	#to csv if True
	if to_csv:
		df.to_csv(filename, index=False)

	return df


if __name__ == '__main__':

	api_key = 'ccb94867375945e89026a2f7819302b8'

	df = get_data(api_key=api_key,
		          project_num=175665,
		          project_name='bballref_player',
		          to_csv=True)