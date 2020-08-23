# Copyright (C) 2014-2019 The BET Development Team

"""
Here, we consider a simple example where a parameter space is given
by a 5-dimensional hypercube and the goal is to choose an optimal QoI
map from a space of possible QoI maps, denoted by :math:`\mathcal{Q}`,
where each QoI map is linear.
We use this simple example to demonstrate the use of the code to
optimally choose which possible QoI map does the best job of "scaling"
inverse sets to smaller sets.
The idea is that if we generally consider a set of high probability
in a particular data space defined by the range of a QoI map, we would
prefer that the inverse of this set is as small as possible in order to
try and identify the parameter responsible for the data.
This only makes sense for stochastic inverse problems framed within the
context of parameter identification under uncertainty.
In other words, when the problem is that the data are uncertain due to
measurement uncertainty and there is a true/exact parameter responsible
for whichever uncertain data is observed, then this is the type of problem
for which this optimization criteria is most appropriate.

This example generates uniform random samples in the unit hypercube and
corresponding QoIs (data) generated by a linear map Q.
We then calculate the gradients using an RBF scheme and use
the gradient information to choose the optimal set of
2 (3, 4, ... input_dim) QoIs to use in the inverse problem.
"""

import numpy as np
import bet.sensitivity.gradients as grad
import bet.sensitivity.chooseQoIs as cqoi
import bet.calculateP.simpleFunP as simpleFunP
import bet.calculateP.calculateP as calculateP
import bet.postProcess.postTools as postTools
import bet.Comm as comm
import bet.sample as sample

# Set up the info for the spaces
input_dim = 5
QoI_scalar_map_num = 10
num_samples = 1E5
num_centers = 10

# Let the map Q be a random matrix of size (QoI_scalar_map_num, input_dim)
np.random.seed(0)
Q = np.random.random([QoI_scalar_map_num, input_dim])

# Initialize some sample objects we will need
input_samples = sample.sample_set(input_dim)
output_samples = sample.sample_set(QoI_scalar_map_num)

# Choose random samples in parameter space to solve the model
input_samples.set_values(np.random.uniform(
    0, 1, [np.int(num_samples), input_dim]))


# Compute the output values with the map Q
output_samples.set_values(Q.dot(input_samples.get_values().transpose()).
                          transpose())

# Calculate the gradient vectors at some subset of the samples.  Here the
# *normalize* argument is set to *True* because we are using *bin_ratio* to
# determine the uncertainty in our data.
cluster_discretization = sample.discretization(input_samples, output_samples)
# We will approximate the jacobian at each of the centers
center_discretization = grad.calculate_gradients_rbf(cluster_discretization,
                                                     num_centers, normalize=True)

# With these gradient vectors, we are now ready to choose an optimal set of
# QoIs to use in the inverse problem, based on minimizing the support of the
# inverse solution (measure).  The most robust method for this is
# :meth:~bet.sensitivity.chooseQoIs.chooseOptQoIs_large which returns the
# best set of 2, 3, 4 ... until input_dim.  This method returns a list of
# matrices.  Each matrix has 10 rows, the first column representing the
# expected inverse measure ratio, and the rest of the columns the corresponding
# QoI indices.
input_samples_center = center_discretization.get_input_sample_set()
best_sets = cqoi.chooseOptQoIs_large(input_samples_center, measure=True)

###############################################################################

# At this point we have determined the optimal set of QoIs to use in the inverse
# problem.  Now we compare the support of the inverse solution using
# different sets of these QoIs.  We set Q_ref to correspond to the center of
# the parameter space.  We choose the set of QoIs to consider.

QoI_indices = best_sets[0][0, 1:].astype(
    int)  # Chooses the optimal set of 2 QoI
# QoI_indices = best_sets[0][1,1:].astype(int) # Chooses the second most optimal set of 2 QoI
# QoI_indices = best_sets[0][9,1:].astype(int) # Chooses the least optimal set of 2 QoI
# QoI_indices = best_sets[3][0,1:].astype(int) # Chooses the optimal set of 5 QoI
# QoI_indices = best_sets[3][1,1:].astype(int) # Chooses the second most
# optimal set of 5 QoI

# Setup the output sample set associated to the QoI choice
output_samples._dim = len(QoI_indices)
output_samples.set_values(output_samples.get_values()[:, QoI_indices])

# Define the reference point in the output space to correspond to the center of
# the input space.
param_ref = 0.5 * np.ones(input_dim)
Q_ref = Q[QoI_indices, :].dot(param_ref)

# Define the level of uncertainty in the measured reference datum
rect_scale = 0.25

# Make the MC assumption and compute the volumes of each voronoi cell
input_samples.estimate_volume_mc()

# Create discretization object
my_discretization = sample.discretization(input_sample_set=input_samples,
                                          output_sample_set=output_samples)


# Find the simple function approximation
simpleFunP.regular_partition_uniform_distribution_rectangle_scaled(
    data_set=my_discretization, Q_ref=Q_ref, rect_scale=rect_scale,
    cells_per_dimension=1)

# Compute the solution to the stochastic inverse problem
calculateP.prob(my_discretization)

percentile = 1.0
# Sort samples by highest probability density and find how many samples lie in
# the support of the inverse solution.  With the Monte Carlo assumption, this
# also tells us the approximate volume of this support.
(num_samples, _, indices_in_inverse) =\
    postTools.sample_highest_prob(top_percentile=percentile,
                                  sample_set=input_samples, sort=True)

# Print the approximate proportion of the measure of the parameter space defined
# by the support of the inverse density
if comm.rank == 0:
    print('The approximate proportion of the measure of the parameter space defined')
    print('by the support of the inverse density associated with the choice of QoI map is')
    print(np.sum(input_samples.get_volumes()[indices_in_inverse]),
          ' with ', num_samples, ' samples.')
