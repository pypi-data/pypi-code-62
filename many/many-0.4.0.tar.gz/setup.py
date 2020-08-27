# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['many', 'many.stats', 'many.visuals']

package_data = \
{'': ['*']}

install_requires = \
['adjusttext>=0.7.3,<0.8.0',
 'flake8>=3.8.3,<4.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.11.1,<0.12.0',
 'tqdm>=4.48.2,<5.0.0']

setup_kwargs = {
    'name': 'many',
    'version': '0.4.0',
    'description': '',
    'long_description': '# many\n\nThis package serves as a general-use toolkit for frequently-implemented statistical and visual methods.\n\n## Installation\n\n```bash\npip install many\n```\n\n## Components\n\n### Statistical methods\n\nThe statistical methods comprise several functions for association mining between variable pairs. The methods used here are optimized for `pandas` DataFrames and are inspired by the `corrcoef` function provided by `numpy`.\n\nBecause these functions rely on native matrix-level operations provided by `numpy`, many are orders of magnitude faster than naive looping-based alternatives. This makes them useful for constructing large association networks or for feature extraction, which have important uses in areas such as biomarker discovery. All methods also return estimates of statistical significance.\n\nIn certain cases such as the computation of correlation coefficients, **these vectorized methods come with the caveat of [numerical instability](https://stats.stackexchange.com/questions/94056/instability-of-one-pass-algorithm-for-correlation-coefficient)**. As a compromise, "naive" loop-based implementations are also provided for testing and comparison. It is recommended that any significant results obtained with the vectorized methods be verified with these base methods.\n\nThe current functions available are listed below by variable comparison type. Benchmarks are also provided with comparisons to the equivalent looping-based method. In all methods, a `melt` option is provided to return the outputs as a set of row-column variable-variable pair statistic matrices or as a single `DataFrame` with each statistic melted to a column.\n\n#### Continuous vs. continuous\n\n```python\nmat_corr(a_mat, b_mat, melt: bool, method: str)\n```\n\nComputes pairwise Pearson or Spearman correlations between columns of `a_mat` and `b_mat`, provided that there are no missing values in either matrix. `method` can be either "pearson" or "spearman".\n\n```python\nmat_corr_nan(a_mat, b_mat, melt: bool, method: str)\n```\n\nComputes pairwise Pearson or Spearman correlations between `a_mat` and the columns of `b_mat`, provided that `a_mat` is a `Series` and `b_mat` is a `DataFrame` that may or may not contain some missing values. `method` can be either "pearson" or "spearman".\n\n```python\nmat_corr_naive(a_mat, b_mat, melt: bool, method: str, pbar=False)\n```\n\nSame functionality as `mat_corr`, but uses a double loop for direct computation of statistics. `method` can be either "pearson" or "spearman".\n\n#### Continuous vs. categorical\n\n```python\nmat_mwu(a_mat, b_mat, melt: bool, effect: str, use_continuity=True)\n```\n\nComputes pairwise Mann-Whitney U tests between columns of `a_mat` (continuous samples) and `b_mat` (binary samples). Assumes that `a_mat` and `b_mat` both do not contain any missing values. `effect` can only be `rank_biserial`. `use_continuity` specifies whether a continuity correction should be applied.\n\n```python\nmat_mwu_naive( a_mat, b_mat, melt: bool, effect: str, use_continuity=True, pbar=False)\n```\n\nSame functionality as `mat_mwu`, but uses a double loop for direct computation of statistics. Unlike `mat_mwus, ` `effect` parameters of "mean", "median", and "rank_biserial" are all supported.\n\n#### Categorical vs. categorical\n\n```python\nmat_fisher(a_mat, b_mat, melt: bool, pseudocount=0)\n```\n\nComputes pairwise Fisher\'s exact tests between columns of `a_mat` and `b_mat`, provided that both are boolean-castable matrices and do not contain any missing values. The `pseudocount` parameter (which must be an integer) specifies the value that should be added to all cells of the contingency matrices.\n\n```python\nmat_fisher_nan(a_mat, b_mat, melt: bool, pseudocount=0)\n```\n\nComputes pairwise Fisher\'s exact tests between columns of `a_mat` and `b_mat`, provided that both are boolean-castable matrices and may or may not contain missing values.\n\n```python\nmat_fisher_naive(a_mat, b_mat, melt: bool, pseudocount=0, pbar=False)\n```\n\nSame functionality as `mat_fisher`, but uses a double loop for direct computation of statistics.\n\n#### Benchmarks\n\nBenchmarks were run with 1,000 samples per variable (i.e. setting each input matrix to have 1,000 rows). The number of variables in `a_mat` was set to 100, and the number of variables in `b_mat` was varied as shown below. The number of pairwise comparisons (equivalent to the product of the column counts of `a_mat` and `b_mat`) is also indicated.\n\nBenchmarks were run on an i7-7700K with 16GB of 2133 MHz RAM.\n\n<p align="center">\n  <img src="https://github.com/kevinhu/many/raw/master/tests/benchmark_plots/all_benchmarks.png">\n</p>\n\n### Visual methods\n\n## Development\n\n1. Install dependencies with `poetry install`\n2. Initialize environment with `poetry shell`\n3. Initialize pre-commit hooks with `pre-commit install`\n',
    'author': 'Kevin Hu',
    'author_email': 'kevinhuwest@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevinhu/many',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
