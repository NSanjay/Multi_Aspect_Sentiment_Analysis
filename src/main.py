from process_data import ProcessData
from model import Model

if __name__ == '__main__':
	pass
	# one module for data preprocessing
	# another module for model construction
	# another for evaulation (k-fold)
	train_data = ProcessData()
	model = Model()
	model.construct_model(train_data.data_frame)

	#test
	test_data = ProcessData(file_name="test.tsv")
	model.evaluate_model(test_data.data_frame)

	