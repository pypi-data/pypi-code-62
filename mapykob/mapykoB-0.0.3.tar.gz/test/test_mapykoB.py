from pytest import fixture
from collections import Counter
import numpy as np

@fixture
def hmm_discreet():
    from mapykoB import hmm_discreet
    return hmm_discreet


def test_compute_alpha(hmm_discreet):

	sample_data = np.array([
		[1, 1, 1, 0, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 1, 0, 1],
		[0, 0, 1, 0, 1, 1, 1, 1],
		[0, 0, 0, 0, 1, 0, 1, 0],
		[0, 1, 0, 0, 1, 1, 0, 1],
		[0, 0, 0, 1, 1, 1, 0, 0]])

	alpha = np.array([
		[0.2       , 0.35      ],
		[0.112     , 0.189     ],
		[0.0616    , 0.1029    ],
		[0.050568  , 0.024066  ],
		[0.0270144 , 0.008883  ],
		[0.01347797, 0.00403024],
		[0.006628  , 0.00193846],
		[0.00324899, 0.00094544]])

	alpha1= alpha.round(decimals=8)
	possible_observations = Counter(sample_data[i][j] for i in range(len(sample_data)) for j in range(len(sample_data[i])))
	M = 2
	V = len(possible_observations)
	hmm_discreet = hmm_discreet(M,sample_data,V)
	hmm_discreet.pi = np.array([0.5, 0.5])
	hmm_discreet.A = np.array([[0.7, 0.3], [0.4, 0.6]])
	hmm_discreet.B = np.array([[0.6, 0.4], [0.3, 0.7]])
	hmm_discreet.compute_alpha(0)
	alpha2=hmm_discreet.alpha.round(decimals=8)
	np.testing.assert_array_equal(alpha1,alpha2)


def test_compute_p_from_alpha(hmm_discreet):

	p1 = 0.004194434664
	sample_data = np.array([
		[1, 1, 1, 0, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 1, 0, 1],
		[0, 0, 1, 0, 1, 1, 1, 1],
		[0, 0, 0, 0, 1, 0, 1, 0],
		[0, 1, 0, 0, 1, 1, 0, 1],
		[0, 0, 0, 1, 1, 1, 0, 0]])

	possible_observations = Counter(sample_data[i][j] for i in range(len(sample_data)) for j in range(len(sample_data[i])))
	M = 2
	V = len(possible_observations)
	hmm_discreet = hmm_discreet(M,sample_data,V)
	hmm_discreet.pi = np.array([0.5, 0.5])
	hmm_discreet.A = np.array([[0.7, 0.3], [0.4, 0.6]])
	hmm_discreet.B = np.array([[0.6, 0.4], [0.3, 0.7]])
	hmm_discreet.compute_alpha(0)
	p2 = hmm_discreet.compute_p_from_alpha(0)
	p2 = p2.round(decimals = 12)
	assert p1 == p2


def test_compute_beta(hmm_discreet):

	sample_data = np.array([
		[1, 1, 1, 0, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 1, 0, 1],
		[0, 0, 1, 0, 1, 1, 1, 1],
		[0, 0, 0, 0, 1, 0, 1, 0],
		[0, 1, 0, 0, 1, 1, 0, 1],
		[0, 0, 0, 1, 1, 1, 0, 0]])

	beta = np.array([[0.00670425, 0.0081531 ],
       [0.01313852, 0.01440698],
       [0.02967516, 0.02299752],
       [0.060588  , 0.04698   ],
       [0.12366   , 0.09612   ],
       [0.252     , 0.198     ],
       [0.51      , 0.42      ],
       [1.        , 1.        ]])
	
	beta1= beta.round(decimals=8)
	possible_observations = Counter(sample_data[i][j] for i in range(len(sample_data)) for j in range(len(sample_data[i])))
	M = 2
	V = len(possible_observations)
	hmm_discreet = hmm_discreet(M,sample_data,V)
	hmm_discreet.pi = np.array([0.5, 0.5])
	hmm_discreet.A = np.array([[0.7, 0.3], [0.4, 0.6]])
	hmm_discreet.B = np.array([[0.6, 0.4], [0.3, 0.7]])
	hmm_discreet.compute_beta(0)
	beta2=hmm_discreet.beta.round(decimals=8)
	np.testing.assert_array_equal(beta1,beta2)


def test_compute_p_from_beta(hmm_discreet):

	p1 = 0.004194434664
	sample_data = np.array([
		[1, 1, 1, 0, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 1, 0, 1],
		[0, 0, 1, 0, 1, 1, 1, 1],
		[0, 0, 0, 0, 1, 0, 1, 0],
		[0, 1, 0, 0, 1, 1, 0, 1],
		[0, 0, 0, 1, 1, 1, 0, 0]])

	possible_observations = Counter(sample_data[i][j] for i in range(len(sample_data)) for j in range(len(sample_data[i])))
	M = 2
	V = len(possible_observations)
	hmm_discreet = hmm_discreet(M,sample_data,V)
	hmm_discreet.pi = np.array([0.5, 0.5])
	hmm_discreet.A = np.array([[0.7, 0.3], [0.4, 0.6]])
	hmm_discreet.B = np.array([[0.6, 0.4], [0.3, 0.7]])
	hmm_discreet.compute_beta(0)
	p2 = hmm_discreet.compute_p_from_beta(0)
	p2 = p2.round(decimals = 12)
	assert p1 == p2


def test_p_from_beta_is_p_from_alpha(hmm_discreet):

	p = 0.004194434664
	sample_data = np.array([
		[1, 1, 1, 0, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 1, 0, 1],
		[0, 0, 1, 0, 1, 1, 1, 1],
		[0, 0, 0, 0, 1, 0, 1, 0],
		[0, 1, 0, 0, 1, 1, 0, 1],
		[0, 0, 0, 1, 1, 1, 0, 0]])

	possible_observations = Counter(sample_data[i][j] for i in range(len(sample_data)) for j in range(len(sample_data[i])))
	M = 2
	V = len(possible_observations)
	hmm_discreet = hmm_discreet(M,sample_data,V)
	hmm_discreet.pi = np.array([0.5, 0.5])
	hmm_discreet.A = np.array([[0.7, 0.3], [0.4, 0.6]])
	hmm_discreet.B = np.array([[0.6, 0.4], [0.3, 0.7]])
	hmm_discreet.compute_alpha(0)
	hmm_discreet.compute_beta(0)
	p1 = hmm_discreet.compute_p_from_alpha(0)
	p2 = hmm_discreet.compute_p_from_beta(0)
	p1 = p1.round(decimals = 12)
	p2 = p2.round(decimals = 12)
	assert p2 == p1 == p
