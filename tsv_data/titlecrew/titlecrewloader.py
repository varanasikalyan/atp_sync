from .df_options import *
from root import engine
import pandas as pd
import os
import gc

def load_tsv_to_sql(file, df_options=None):
	"""Get path of the tsv file to load"""	
	tsv_path = get_tsv_path('tsv_data\\{0}'.format(file))
	
	for key, value in df_options.items():
		"""Loading initial dataframe"""
		print('Pulling the latest data for table: {0} from tsv.'.format(key))
		df = pd.read_csv(tsv_path, sep='\t', usecols=value['columns'], encoding='utf-8')
	
		"""Cleaning \\N values in year with None"""
		if 'mapping' in value.keys():
			df = df.applymap(lambda s: value['mapping'].get(s) if s in value['mapping'] else s)

		"""Set the appropriate datatypes to the columns"""
		df = df.astype(value['dtype'], copy=True)

		"""Dumping the data into database"""
		print('Dumping the latest data for table: {0} from tsv into db.'.format(key))
		df.to_sql(key, con=engine, if_exists='replace')

		"""Dispose dataframe"""
		del df
		gc.collect()

def get_tsv_path(file):	
	folder = os.path.join(os.getcwd(), file)	
	return os.path.join(folder, os.listdir(folder)[0])

load_tsv_to_sql('titlecrew', df_options)