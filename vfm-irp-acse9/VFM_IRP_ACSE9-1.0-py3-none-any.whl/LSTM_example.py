# Original dataset and code coming from machinelearningmastery.com,
# adapted for Wintershall by TNO.

import matplotlib.pyplot as plt
from pandas import read_csv
import math
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


def main(data_file, LSTM_units, lbck, epochs, training_split):

    # Fix random seed for reproducibility
    np.random.seed(7)

    # Load dataset. Number of columns needs to be changed if more features are used.
    dataframe = read_csv(data_file, usecols=[1],
                         engine='python')
    dataset = dataframe.values
    dataset = dataset.astype('float32')

    # Normalize dataset.
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    # Split into train and test sets
    train_size = int(len(dataset) * training_split)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

    # Reshape into X=t and Y=t+1
    trainX, trainY = create_dataset(train, lbck)
    testX, testY = create_dataset(test, lbck)

    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    # Create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(LSTM_units, input_shape=(1, lbck)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=epochs, batch_size=1, verbose=2)

    # Make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    # Invert predictions (scale back to original dimensions).
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])

    # Calculate Root Mean Squared error
    trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
    print('Test Score: %.2f RMSE' % (testScore))

    # Shift train predictions for plotting
    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[lbck-1:len(trainPredict) + lbck-1, :]\
        = trainPredict

    # Shift test predictions for plotting
    testPredictPlot = np.empty_like(dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict)+(lbck*2):len(dataset)-2,:]\
        = testPredict

    # plot baseline and predictions
    plt.plot(scaler.inverse_transform(dataset))
    plt.plot(trainPredictPlot, label='Train set')
    plt.plot(testPredictPlot, label='Test set')
    plt.legend()
    plt.show()

    print("Finished with LSTM model.")



# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)


if __name__ == '__main__':

    ### Define simulation parameters.

    # Data file.
    # The format of the data file should be:
    # - First column: feature (input).
    # - Second column: label (output).
    # Test dataset using number of passangers for an airline for several years.
    data_file = r'N:\_wino\Production and Development\NWoW\Coding Hour\XXXX.csv'

    # Number of LSTM units.
    LSTM_units = 20

    # Lookback window: number of samples from the past used as a sequence (>0).
    lookback_window = 1

    # Number of epochs to train.
    epochs = 20

    # Training/test data split (percentage of data to train with respect to
    # total dataset).
    training_split = 0.70

    print("Executing LSTM sample code...")

    main(data_file, LSTM_units, lookback_window, epochs, training_split)

