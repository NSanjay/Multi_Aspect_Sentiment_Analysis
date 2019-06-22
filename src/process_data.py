from typing import List
import csv
import os
import pandas as pd
import numpy as np

class ProcessData(object):
	def __init__(self, file_name: str = 'train.tsv', data_dir: str = '../data/drugLib_raw'):
		data_file_path = os.path.join(data_dir,file_name)
		self._tsv_data = pd.read_csv(data_file_path,sep='\t')
		self._convert_ratings_to_numbers()
		self._preprocess_text()
		columns = ['combined_reviews','overall_ratings_num']
		self.data_frame = self._tsv_data[columns]

	def _convert_ratings_to_numbers(self):
		effectiveness_ratings_map = {"Ineffective":0,"Marginally Effective":1,"Moderately Effective":1,"Considerably Effective":2,"Highly Effective":2}
		self._tsv_data['effectiveness_num'] = self._tsv_data['effectiveness'].map(effectiveness_ratings_map).fillna(1).astype(int)

		

		side_effects_ratings_map = {"No Side Effects":0,"Mild Side Effects":1,"Moderate Side Effects":1,"Severe Side Effects":2,"Extremely Severe Side Effects":2}
		self._tsv_data['sideEffects_num'] = self._tsv_data['sideEffects'].map(side_effects_ratings_map).fillna(1).astype(int)

		criteria = [self._tsv_data['rating'].between(1, 4), self._tsv_data['rating'].between(5, 6), self._tsv_data['rating'].between(7, 10)]
		overall_ratings_map = [-1, 0, 1]

		self._tsv_data['overall_ratings_num'] = np.select(criteria, overall_ratings_map, 0)

		#Drop those columns
		#self._tsv_data.drop('effectiveness',1,inplace=True)
		#self._tsv_data.drop('sideEffects',1,inplace=True)
		#self._tsv_data.drop('rating',1,inplace=True)

	def _preprocess_text(self):
		#print(self._tsv_data.iloc[147]['commentsReview'].astype(str).isnull())
		self._tsv_data = self._tsv_data[self._tsv_data['commentsReview'].notnull()]
		self._tsv_data = self._tsv_data[self._tsv_data['sideEffectsReview'].notnull()]
		self._tsv_data = self._tsv_data[self._tsv_data['benefitsReview'].notnull()]

		
		self._tsv_data['combined_reviews'] = self._tsv_data['benefitsReview'] + "." +  self._tsv_data['sideEffectsReview'] + "." + self._tsv_data['commentsReview']

		#replace digits
		self._tsv_data['combined_reviews'].replace(to_replace='\d+',value='',regex=True,inplace=True)

		#replace special characters
		self._tsv_data['combined_reviews'].replace(to_replace='[!@#$%^&*()-_=+<>/?;\'\"/\\:]',value='',regex=True,inplace=True)

		# Drop those columns
		#self._tsv_data.drop('benefitsReview',1,inplace=True)
		#self._tsv_data.drop('sideEffectsReview',1,inplace=True)
		#self._tsv_data.drop('commentsReview',1,inplace=True)

