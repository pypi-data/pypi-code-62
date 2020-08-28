import pysplash
import os
import h5py
import matplotlib.pyplot as plt

test_dir = os.path.dirname(os.path.realpath(__file__))

test_file_binary = os.path.join(test_dir, 'data/fulldump_00000')

data_binary = pysplash.read.read_data(test_file_binary, filetype='Phantom')

data_binary_as_hdf5 = data_binary.as_hdf5

test_snap = "test_save.h5"

data_binary.save_hdf5(test_snap)


import plonk
snap = plonk.load_snap(test_snap)

snap.set_units(position='au', density='g/cm^3', projection='cm')

snap.image(
    quantity='density',
    x='x',
    y='z',
    interp='slice',
    cmap='gist_heat',
)

plt.show()
