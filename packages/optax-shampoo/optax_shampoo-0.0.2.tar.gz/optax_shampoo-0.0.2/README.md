Optimization in machine learning, both theoretical and applied, is presently dominated by first-order gradient methods such as stochastic gradient descent. Second-order optimization methods, that involve second derivatives and/or second order statistics of the data, are far less prevalent despite strong theoretical properties, due to their prohibitive computation, memory and communication costs.

Here we present a scalable implementation of a second-order preconditioning method (concretely, a variant of full-matrix Adagrad) that provides significant convergence and wall-clock time improvements compared to conventional first-order methods on state-of-the-art deep models.

Paper preprints: https://arxiv.org/abs/2002.09018
