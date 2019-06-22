from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

class Model(object):
	def __init__(self):
		
		self._vectorizer = CountVectorizer(stop_words='english',ngram_range=(1,3))

	def construct_model(self,data):
		#print(self._data_frame[self._data_frame['combined_reviews'].isnull()])
		_X = self._vectorizer.fit_transform(data['combined_reviews'])
		_Y = data['overall_ratings_num']
		self.model = LogisticRegression(random_state=0, solver='lbfgs',
								multi_class='multinomial').fit(_X, _Y)
		print("train accuracy:::",self.model.score(_X,_Y))

	def evaluate_model(self,data):
		_X_test = self._vectorizer.transform(data['combined_reviews'])
		_Y_test = data['overall_ratings_num']
		print("test accuracy:::",self.model.score(_X_test,_Y_test))

