import pysplashsph
import os

print("********* FULL DUMP **************")

test_dir = os.path.dirname(os.path.realpath(__file__))

test_file_hdf5 = os.path.join(test_dir, 'data/fulldump_00000.h5')

data_hdf5 = pysplashsph.read.read_data(test_file_hdf5, filetype='Phantom', use_HDF5=True)

test_file_binary = os.path.join(test_dir, 'data/fulldump_00000')

data_binary = pysplashsph.read.read_data(test_file_binary, filetype='Phantom')

print("***** BINARY DATA HEADER ")

print(data_binary['header'])

data_binary_as_hdf5 = data_binary.as_hdf5

# print('Real HDF5', data_hdf5.keys())
# print('Real HDF5',data_hdf5['particles'].keys())
# print('My HDF5', data_binary_as_hdf5['particles'].keys())

print('Real HDF5 sinks', data_hdf5['sinks'].keys())
print('My HDF5 sinks', data_binary_as_hdf5['sinks'].keys())

# print('Real HDF5', data_hdf5['header'])
# print('Real HDF5', data_hdf5['header'].keys())
# print('Real HDF5', data_hdf5['header/Bextx'][()])
#
# print('My HDF5', data_binary_as_hdf5['header'])
# print('My HDF5', data_binary_as_hdf5['header'].keys())
# print('My HDF5', data_binary_as_hdf5['header/Bextx'][()])



print("********* SMALL DUMP **************")

test_dir = os.path.dirname(os.path.realpath(__file__))

test_file_hdf5 = os.path.join(test_dir, 'data/smalldump_00000.h5')

data_hdf5 = pysplashsph.read.read_data(test_file_hdf5, filetype='Phantom', use_HDF5=True)

test_file_binary = os.path.join(test_dir, 'data/smalldump_00000')

data_binary = pysplashsph.read.read_data(test_file_binary, filetype='Phantom')

data_binary_as_hdf5 = data_binary.as_hdf5

# print('Real HDF5', data_hdf5.keys())
# print('Real HDF5',data_hdf5['particles'].keys())
# print('My HDF5', data_binary_as_hdf5['particles'].keys())

print('Real HDF5 sinks', data_hdf5['sinks'].keys())
print('My HDF5 sinks', data_binary_as_hdf5['sinks'].keys())

for key in data_hdf5['particles'].keys():
    print(data_hdf5['particles'][key])

print('*******')

for key in data_binary_as_hdf5['header'].keys():
    print(data_binary_as_hdf5['header'][key])
    print(data_binary_as_hdf5['header'][key].value)


print(data_hdf5['header/massoftype'])

# print('Real HDF5', data_hdf5['header'])
# print('Real HDF5', data_hdf5['header'].keys())
# print('Real HDF5', data_hdf5['header/Bextx'][()])
#
# print('My HDF5', data_binary_as_hdf5['header'])
# print('My HDF5', data_binary_as_hdf5['header'].keys())
# print('My HDF5', data_binary_as_hdf5['header/Bextx'][()])
