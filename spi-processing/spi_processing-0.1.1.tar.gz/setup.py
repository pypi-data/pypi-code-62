from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='spi_processing',
      version='0.1.1',
      description='Module for processing of diffraction images in CXI format.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://gitlab.com/spi_xfel/spi_processing',
      author='Sergey Bobkov',
      author_email='s.bobkov@grid.kiae.ru',
      license='MIT',
      python_requires='>=3.6',
      install_requires=['numba',
                        'numpy',
                        'scipy',
                        'matplotlib',
                        'pandas',
                        'h5py',
                        'tqdm'],
      packages=['spi_processing'],
      scripts=['scripts/spi_combine.py',
               'scripts/spi_compute_photons.py',
               'scripts/spi_correct_background.py',
               'scripts/spi_estimate_center.py',
               'scripts/spi_estimate_size.py',
               'scripts/spi_filter.py',
               'scripts/spi_plot_histogram.py',
               'scripts/spi_refine_center.py',
               'scripts/spi_set_center.py'],
      zip_safe=False)
