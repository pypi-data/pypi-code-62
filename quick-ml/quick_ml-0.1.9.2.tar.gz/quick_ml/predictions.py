## function for obtaining predictions
def get_predictions(GCS_DS_PATH, test_tfrec_path, BATCH_SIZE, model, output_filename):
	import numpy as np

	testdata = get_test_dataset(GCS_DS_PATH, test_tfrec_path, BATCH_SIZE):
	images = testdata.map(lambda image, idnum : image)
	ids = testdata.map(lambda image, idnum : idnum).unbatch()

	NUM_TEST_IMAGES = 0
	for data in testdata:
		NUM_TEST_IMAGES += 1

	probabilities = model.predict(images)
	predictions = np.argmax(probabilities,axis = 1)
	print("Generating Output File...")
	ids = next(iter(ids.batch(NUM_TEST_IMAGES))).numpy().astype('U')
	np.savetxt(output_filename, np.rec.fromarrays([ids, predictions]), fmt = ['%s', '%d'], delimiter = ',', header = 'id,label', comments = '')
	print(f"predictions obtained with filename as {output_filename}")


def get_predictions(testTFdataset, model, output_filename):
	import numpy as np
	images = testTFdataset.map(lambda image, idnum : image)
	ids = testTFdataset.map(lambda image, idnum : idnum).unbatch()

	NUM_TEST_IMAGES = 0
	for data in testTFdataset:
		NUM_TEST_IMAGES += 1

	probabilities = model.predict(images)
	predictions = np.argmax(probabilities, axis = 1)
	print("Generating Output File..")
	ids = next(iter(ids.batch(NUM_TEST_IMAGES))).numpy().astype('U')
	np.savetxt(output_filename, np.rec.fromarrays([ids, predictions]), fmt = ['%s', '%d'], delimiter = ',', header = 'id,label', comments = '')
	print(f"predictions obtained with filename as -> {output_filename}")


	
## functions for ensembling using Models
def ensemble_model_average(models_list, testTFdataset):
	import numpy as np

	test_images_ds = testTFdataset.map(lambda image, idnum : image)

	probs = np.average([models_list[i].predict(test_images_ds) for i in range(len(models_list))], axis = 0)
	preds = np.argmax(probs, axis = -1)

	return preds

def ensemble_model_weighted(weights, models_list, testTFdataset):
	
	probs = []
	test_images_ds = testTFdataset.map(lambda image, idnum : image)

	for model in models_list:
		probs.append(model.predict(test_images_ds))

	final_probs = None
	for i, w in enumerate(weights):
		final_probs = w * probs[i]

	preds = np.argmax(final_probs, axis = -1)	
	return preds


def ensemble_predictions(ensemble_type = 'Model Averaging', models_list,  testTFdataset):
	if ensemble_type == 'Model Averaging':
		print("Computing predictions through Model Averaging")
		preds =  ensemble_model_average(models_list, testTFdataset)
		print("Generating output file...")

		ids = testTFdataset.map(lambda image, idnum : idnum).unbatch()

		NUM_TEST_IMAGES = 0
		for data in testTFdataset:
			NUM_TEST_IMAGES += 1

		ids = next(iter(ids.batch(NUM_TEST_IMAGES))).numpy().astype('U')
		np.savetxt('ensemble_model_averaging.csv', np.rec.fromarrays([ids, predictions]), fmt = ['%s', '%d'], delimiter = ',', header = 'id,label', comments = '')
		print("Predictions obtained with the output filename as -> ensemble_model_average")

	elif ensemble_type == 'Model Weighted':
		print("Please enter the weights by which the models should be ensembled.(sum = 1) Format -> comma seperated -> ")
		weights = input()
		weights = weights.split(',')
		weights = [float(i) for i in weights]

		print("Computing predictions through Model Weighted")
		preds =  ensemble_model_weighted(weights, models_list, testTFdataset)

		print("Generating output file...")

		ids = testTFdataset.map(lambda image, idnum : idnum).unbatch()

		NUM_TEST_IMAGES = 0
		for data in testTFdataset:
			NUM_TEST_IMAGES += 1

		ids = next(iter(ids.batch(NUM_TEST_IMAGES))).numpy().astype('U')
		np.savetxt('ensemble_model_weighted.csv', np.rec.fromarrays([ids, predictions]), fmt = ['%s', '%d'], delimiter = ',', header = 'id,label', comments = '')
		print("Predictions obtained with the output filename as -> ensemble_model_weighted.csv")


	else:
		print("Please choose ensemble_type between 'Model Averaging' or 'Model Weighted'")
		return

	#return preds



## function for having test time augmentations
def test_time_augmentations():
	print("Feature Coming Soon!")


if __name__ == '__main__':
	pass
else:
	import os
	os.system('pip install tensorflow==2.2.0')
	import tensorflow as tf 
	import numpy as np
	if tf.__version__ == '2.2.0':
		pass
	else:
		print("Tensorflow version mismatch. Either pip install tf version as specified in the docs or import the libraries in the beginning.")
