# perform various data augmentations 

def define_augmentations(flip_left_right = False, hue = None, contrast = None, brightness = None):
	
	

	augments = {}

	if flip_left_right:
		augments['flip_left_right'] = True

	if hue:
		augments['random_hue'] = hue


	if contrast:
		if isinstance(contrast, tuple):
			augments['random_contrast'] = contrast

	if brightness:
		augments['brightness'] = brightness


	if len(list(augments.items())) == 0:
		print("Error! No augments defined...")
		return



def augmentations(image, label):

	
	for aug in augments.items():
		if aug[0] == 'flip_left_right' and aug[1] == True:
			image = tf.image.random_flip_left_right(image)
		if aug[0] == 'hue':
			image = tf.image.random_hue(image, aug[1])
		if aug[0] == 'contrast':
			image = tf.image.random_contrast(image, aug[1][0], aug[1][1])
		if aug[0] == 'brightness':
			image = tf.image.random_brightness(image, aug[1])

	return image, label




def augment_and_training_report(models_list, GCS_DS_PATH, train_tfrec_path, val_tfrec_path, batch_size, tpu, n_class, steps_per_epoch, epochs, classification_model = 'default', freeze = False, input_shape = [512,512,3], activation = 'softmax', weights = "imagenet", optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = "sparse_categorical_accuracy", callbacks = None, plot = False):


	import pandas as pd
	import numpy as np
	import gc
	from quick_ml.load_models_quick import create_model
	print("Num classes => " , n_class)
	print("\n\n", '#'*90, '\n\n')
	print("\n\n TO OBTAIN THE BEST PERFORMANCE, PLEASE USE THE PRETRAINED MODEL WEIGHTS AS INPUT. Dataset Link -> https://www.kaggle.com/superficiallybot/tf-keras-pretrained-weights\n\n")
	print("\n\n", '#'*90, '\n\n')
	
	df = pd.DataFrame(columns = ['Model_Name', 'Accuracy_top1', 'Accuracy_top3', "Val_Accuracy_top1", "Val_Accuracy_top3"])

	for m in models:
		print(f"Beginning with model -> {m}")
		tf.tpu.experimental.initialize_tpu_system(tpu)
		strategy = tf.distribute.experimental.TPUStrategy(tpu)
		with strategy.scope():
			if classification_model != 'default':
				model = create_model( freeze = freeze, input_shape = input_shape, activation = activation, weights = weights, optimizer = optimizer, loss = loss, metrics = metrics, classes = n_class, model_name = m, classification_model = classification_model)
			else:
				model = create_model( freeze = freeze, input_shape = input_shape, activation = activation, weights = weights, optimizer = optimizer, loss = loss, metrics = metrics , classes = n_class, model_name = m)
				
		from quick_ml.begin_tpu import get_training_dataset, get_validation_dataset
		history = model.fit(get_training_dataset(GCS_DS_PATH, train_tfrec_path, batch_size, augmentation = True), get_validation_dataset(GCS_DS_PATH, val_tfrec_path, batch_size, augmentation = True), steps_per_epoch = steps_per_epoch, epochs = epochs,batch_size = batch_size, validation_data =  val_data, callbacks = callbacks, verbose = 0)
		tf.keras.backend.clear_session()
		tf.compat.v1.reset_default_graph()
		del model
		gc.collect()
		

		df = df.append(pd.DataFrame([[m, history.history[metrics][-1], np.mean(history.history[metrics][-3:]) , history.history['val_' + metrics][-1], np.mean(history.history['val_' + metrics][-3:])]], columns = ['Model_Name', 'Accuracy_top1', 'Accuracy_top3', "Val_Accuracy_top1", "Val_Accuracy_top3"]), ignore_index = True)
		print(f"Done with model -> {m}")

	if plot:

		print("Plotting Feature Coming soon...")

		## under making
		"""import matplotlib.plt as plt
		import seaborn as sns

		sns.lineplot(x = list(range(1,epochs + 1)), y = histories[0].history[metrics], label = 'Training Accuracy');
		sns.lineplot(x = list(range(1,epochs + 1)), y = histories[0].history['val_' + metrics], label = 'Validation Accuracy').set_title(f'{metrics} Plot vs Epoch');
		plt.show()"""

	return df



def augment_and_train(model, GCS_DS_PATH, train_tfrec_path, val_tfrec_path, batch_size, epochs, steps_per_epoch, callbacks = None, plot = False):

	from quick_ml.begin_tpu import get_training_dataset
	from quick_ml.begin_tpu import get_validation_dataset

	history = model.fit(get_training_dataset(GCS_DS_PATH, train_tfrec_path, batch_size, augmentation = True), validation_data = get_validation_dataset(GCS_DS_PATH, val_tfrec_path, batch_size, augmentation = True), epochs = epochs, steps_per_epoch = steps_per_epoch, batch_size = batch_size, verbose = 1, callbacks = callbacks)

	if plot:
		import matplotlib.pyplot as plt
		import seaborn as sns

		keys = history.keys()

		sns.lineplot(x = list(range(1, epochs + 1)), y = history[keys[0]], label = 'Training Accuracy');
		sns.lineplot(x = list(range(1, epochs + 1)), y = history[keys[2]], label = 'Validation Accuracy');
		plt.show()


    




if __name__ == "__main__":
	pass
else:
	import tensorflow as tf
	global augments
	if tf.__version__ == '2.2.0':
		pass
	else:
		print("Error! Tensorflow Version mismatch. Please refer to the documentation to know the supported version of tensorflow.")