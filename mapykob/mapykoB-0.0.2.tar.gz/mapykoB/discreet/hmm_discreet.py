import numpy as np


class hmm_discreet(object):
    """An exemple of discreet Hidden Markov Model. """

    def __init__(self, M, X, V):
        r"""Initialize a discreet Hidden Markov Model.

        Arguments :
            M -- the number of states
            X -- the observation sequences
            V -- the number of symbols
        """
        self.T_MAX = 250
        self.T_INC = 10
        self.M = M
        self.X = X
        self.V = V
        self.N = len(X)
        self.T = len(X[0])
        self.alpha = np.zeros((self.T, self.M))
        self.beta = np.zeros((self.T, self.M))
        self.A = np.ones((self.M, self.M))
        self.B = np.ones((self.M, self.V))
        self.pi = np.ones(self.M)
        self.alphas = []
        self.betas = []
        self.P = np.zeros(self.N)
        self.scales = []
        self.logP = np.zeros(self.N)
        self.gamma = np.ones((self.T, self.M))
        self.xi = np.ones((self.T, self.M, self.M))
        

    @staticmethod
    def normalized_matrix(m):
        r"""Normalize a matrix.

        Arguments :
            m -- the matrix to normalize
        """

        if len(m.shape) > 1:
            return m / m.sum(axis=1, keepdims=True)
        elif len(m.shape) == 1:
            return m / m.sum(axis=0, keepdims=True)
        else:
            return ValueError("Reload Matrix")

    @staticmethod
    def random_matrix_normalized(dim1, dim2=0):
        r"""Normalize a vector or a matrix.

        Arguments :
            dim1 -- the first dimension of the matrix

        Keywords Arguments :
            dim2 -- the second dimension of the matrix
        """
        
        if dim2 == 0:
            v = np.random.random(dim1)
            return v / v.sum(axis=0, keepdims=True)
        else:
            m = np.random.random((dim1, dim2))
            return m / m.sum(axis=1, keepdims=True)

    def compute_alpha(self, seq_idx):
        r"""Compute alpha matrix of a given observation sequence.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: $\alpha({t+1,}{j})=(b[j,O[t+1]].\sum_{i=1}^{N}(a_{i,j}.\alpha({t},{i})) , \forall t \in [1,T-1], \forall j \in [1,N]$
        """

        x = self.X[seq_idx]
        self.T = len(x)
        for i in range(self.M):
            self.alpha[0][i] = self.B[i][x[0]]*self.pi[i]
        for t in range(1, self.T):
            for j in range(self.M):
                s = 0
                for i in range(self.M):
                    s += self.A[i][j]*self.alpha[t-1][i]
                self.alpha[t][j] = self.B[j][x[t]]*s
        self.alphas.append(self.alpha.copy())

    def compute_alpha_scaled(self, seq_idx):
        r"""Compute alpha scaled matrix of a given observation sequence.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: $\alpha({t+1,}{j})=(b[j,O[t+1]].\sum_{i=1}^{N}(a_{i,j}.\alpha({t},{i})) , \forall t \in [1,T-1], \forall j \in [1,N]$
        """

        x = self.X[seq_idx]
        self.T = len(x)
        scale = np.zeros(self.T)
        for i in range(self.M):
            self.alpha[0][i] = self.B[i][x[0]]*self.pi[i]

        print(self.alpha[0])
        scale[0] = self.alpha[0].sum()
        self.alpha[0] /= scale[0]
        print(self.alpha[0])
        for t in range(1, self.T):
            for j in range(self.M):
                s = 0
                for i in range(self.M):
                    s += self.A[i][j]*self.alpha[t-1][i]
                self.alpha[t][j] = self.B[j][x[t]]*s
            scale[t] = self.alpha[t].sum()
            self.alpha[t] = self.alpha[t] / scale[t]

        self.alphas.append(self.alpha.copy())
        self.scales.append(scale)

    def compute_p_from_alpha(self, seq_idx):
        r"""Compute probability of observing a sequence from alpha.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: # $P(X(1,...,T) / H)=\sum_{i=1}^{N}\alpha({T},{i}))$
        """
        
        p = self.alpha[-1].sum()
        self.P[seq_idx] = p
        return p

    def compute_logp_from_alpha(self, seq_idx):
        r"""Compute log probability of observing a sequence from alpha.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: # $P(X(1,...,T) / H)=\sum_{i=1}^{N}\alpha({T},{i}))$
        """
        p = self.scales[seq_idx][self.T-1].sum()
        self.logP[seq_idx] = p
        return p

    def compute_beta(self, seq_idx):
        r"""Compute bêta matrix of a given observation sequence.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: $\beta({t-1,}{i})=\sum_{j=1}^{N}(a(i,j)*b(j,o_{t})*\beta(t,j))$  $\forall$ T $\in$ [T-1, T-2, ...,1] and $\forall$ i $\in$ [1,N]$
        """
        
        x = self.X[seq_idx]
        self.T = len(x)
        for i in range(self.M):
            self.beta[self.T-1][i] = 1
        for t in reversed(range(1, self.T)):
            for i in range(self.M):
                s = 0
                for j in range(self.M):
                    s += self.A[i][j]*self.B[j][x[t]]*self.beta[t][j]
                self.beta[t-1][i] = s
        self.betas.append(self.beta.copy())

    def compute_p_from_beta(self, seq_idx):
        r"""Compute probability of observing a sequence from bêta.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: # $P(X(1,...,T) / H)=\sum_{i}\Pi_{i}*b(i,o_{1})*\beta(1,i)$
        """
        
        x = self.X[seq_idx]
        p = np.sum(self.beta[0][:]*self.B[:, x[0]] * self.pi)
        self.P[seq_idx] = p
        return p

    def compute_p_from_alpha_beta(self, t=None):
        r"""Compute probability of observing a sequence from alpha and bêta.

        Keywords Arguments:
            t -- the time index, Default : None
        Latex:
            Equation: $P(X(1,...,T) / H)=\sum_{i}\alpha(t,i)*beta(t,i)$
        """

        if t != None:
            t = t
        else:
            t = np.random.choice(self.T)
        p = np.sum(self.alpha[t][:]*self.beta[t][:])
        return p

    def compute_gamma(self, seq_idx):
        r"""Compute gamma matrix of a given observation sequence.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: $\gamma(t,i)=\alpha(t,i)*\beta(t,i)/(\sum_{i=1}^{N}\alpha(t,i)*\beta(t,i))$
        """

        p = self.P[seq_idx]
        alpha = self.alphas[seq_idx]
        beta = self.betas[seq_idx]
        for t in range(self.T):
            self.gamma[t][:] = (alpha[t][:]*beta[t][:])/p

    def compute_gamma_scaled(self, seq_idx):
        r"""Compute gamma scaled matrix of a given observation sequence.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: $\gamma(t,i)=\alpha(t,i)*\beta(t,i)/(\sum_{i=1}^{N}\alpha(t,i)*\beta(t,i))$
        """

        p = self.P[seq_idx]
        alpha = self.alphas[seq_idx]
        beta = self.betas[seq_idx]
        for t in range(self.T):
            self.gamma[t][:] = (alpha[t][:]*beta[t][:])

    def compute_xi(self, seq_idx): 
        r"""Compute xi matrix of a given observation sequence.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: $\xi(t,i,j)=\frac{\alpha(t,i)*a_{i,j}*b{j,X_{t+1}}*\beta(t+1,j)}{p(X/\lambda)}$
        """

        p = self.P[seq_idx]
        x = self.X[seq_idx]
        alpha = self.alphas[seq_idx]
        beta = self.betas[seq_idx]
        for i in range(self.M):
            for j in range(self.M):
                for t in range(self.T-1):
                    self.xi[t, i, j] = (
                        alpha[t, i] * self.A[i, j] * self.B[j, x[t+1]] * beta[t+1, j])/p

    def compute_xi_scaled(self, seq_idx):
        r"""Compute xi matrix of a given observation sequence.

        Arguments:
            seq_idx -- the index of the observed sequence
        
        Latex:
            Equation: $\xi(t,i,j)=\frac{\alpha(t,i)*a_{i,j}*b{j,X_{t+1}}*\beta(t+1,j)}{p(X/\lambda)}$
        """

        p = self.P[seq_idx]
        x = self.X[seq_idx]
        alpha = self.alphas[seq_idx]
        beta = self.betas[seq_idx]

        for i in range(self.M):
            for j in range(self.M):
                for t in range(self.T-1):
                    self.xi[t, i, j] = (
                        alpha[t, i] * self.A[i, j] * self.B[j, x[t+1]] * beta[t+1, j])/self.scales[seq_idx][t+1]

    def reestimate_A(self, n):
        r"""Reevaluate A matrix using Baum-Welch re-estimation formulas.

        Arguments:
            n -- the time index
        
        Latex:
            Equation: $\hat a_{i,j}=\frac{\sum_{t=1}^{T-1}\xi(t,i,j)}{\sum_{t=1}^{T-1}\gamma(t,i)}$
        """

        num = 0
        den = 0
        den += (self.alphas[n][:-1] * self.betas[n][:-1]
                ).sum(axis=0, keepdims=True).T / self.P[n]
        self.compute_xi(n)
        for t in range(self.T-1):
            num += self.xi[t, :, :]
        return num, den

    def reestimate_A_scaled(self, n):
        r"""Reevaluate A matrix using Baum-Welch re-estimation formulas.

        Arguments:
            n -- the time index
        
        Latex:
            Equation: $\hat a_{i,j}=\frac{\sum_{t=1}^{T-1}\xi(t,i,j)}{\sum_{t=1}^{T-1}\gamma(t,i)}$
        """

        num = 0
        den = 0
        den += (self.alphas[n][:-1] * self.betas[n]
                [:-1]).sum(axis=0, keepdims=True).T
        self.compute_xi_scaled(n)
        for t in range(self.T-1):
            num += self.xi[t, :, :]
        return num, den

    def reestimate_B(self, n):
        r"""Reevaluate B matrix using Baum-Welch re-estimation formulas.

        Arguments:
            n -- the time index
        
        Latex:
            Equation: $\hat b_{j,k}=\frac{\sum_{t=1,o_t=k}^{T}\gamma(t,j)}{\sum_{t=1}^{T}\gamma(t,j)}$
        """

        num = np.zeros((self.M, self.V))
        den = 0
        x = self.X[n]
        den += (self.alphas[n] * self.betas[n]
                ).sum(axis=0, keepdims=True).T / self.P[n]
        self.compute_gamma(n)
        for t in range(self.T):
            num[:, x[t]] += self.gamma[t][:]
        return num, den

    def reestimate_B_scaled(self, n):
        r"""Reevaluate B matrix using Baum-Welch re-estimation formulas.

        Arguments:
            n -- the time index
        
        Latex:
            Equation: $\hat b_{j,k}=\frac{\sum_{t=1,o_t=k}^{T}\gamma(t,j)}{\sum_{t=1}^{T}\gamma(t,j)}$
        """

        num = np.zeros((self.M, self.V))
        den = 0
        x = self.X[n]
        den += (self.alphas[n] * self.betas[n]).sum(axis=0, keepdims=True).T
        self.compute_gamma_scaled(n)
        for t in range(self.T):
            num[:, x[t]] += self.gamma[t][:]
        return num, den

    def Baum_Welch_Algorithm(self,A_init=None,B_init=None,pi_init=None,max_iter=1):
        r"""Reevaluate A,B,Pi matrix using Baum-Welch re-estimation formulas.

        Arguments:
            A_init -- the initial A matrix
            B_init -- the initial B matrix
            pi_init -- the initial Pi matrix
            max_iter -- the maximim nunber of iteration
        """

        if (A_init, B_init, pi_init) != (None, None, None):
            self.A = normalized_matrix(A_init)
            self.B = normalized_matrix(B_init)
            self.pi = normalized_matrix(pi_init)
        else:
            self.A = random_matrix_normalized(self.M,self.M)
            self.B = random_matrix_normalized(self.M,self.V)
            self.pi = random_matrix_normalized(self.M)

        self.costs = []
        # iteration loop
        for i in range(max_iter):
            
            num_A = 0
            den_A = 0
            num_B = np.zeros((self.M, self.V))
            den_B = 0
            pi = np.zeros(self.M)
            self.alphas = []
            self.betas = []
            self.P = np.zeros(self.N)

            for n in range(self.N):

                self.compute_alpha(n)
                self.compute_p_from_alpha(n)
                self.compute_beta(n)
                pi += (self.alphas[n][0] * self.betas[n][0])/self.P[n]
                numA, denA = self.reestimate_A(n)
                num_A += numA
                den_A += denA
                numB, denB = self.reestimate_B(n)
                num_B += numB
                den_B += denB
                self.costs.append(np.sum(self.P.copy()))

            self.pi = pi / self.N
            self.A = num_A / den_A
            self.B = num_B / den_B

    def Baum_Welch_Algorithm_scaled(self,A_init=None,B_init=None,pi_init=None,max_iter=1):
        r""" eevaluate A,B,Pi matrix using Baum-Welch re-estimation formulas.

        Arguments:
            A_init -- the initial A matrix
            B_init -- the initial B matrix
            pi_init -- the initial Pi matrix
            max_iter -- the maximim nunber of iteration
        """

        if (A_init, B_init, pi_init) != (None, None, None):
            self.A = normalized_matrix(A_init)
            self.B = normalized_matrix(B_init)
            self.pi = normalized_matrix(pi_init)
        else:
            self.A = random_matrix_normalized(self.M,self.M)
            self.B = random_matrix_normalized(self.M,self.V)
            self.pi = random_matrix_normalized(self.M)

        self.costs = []
        # iteration loop
        for i in range(max_iter):

            num_A = 0
            den_A = 0
            num_B = np.zeros((self.M, self.V))
            den_B = 0
            pi = np.zeros(self.M)
            self.alphas = []
            self.betas = []
            self.scales = []
            self.logP = np.zeros(self.N)

            for n in range(self.N):
                self.compute_alpha_scaled(n)
                self.compute_logp_from_alpha(n)
                self.compute_beta_scaled(n)
                pi += (self.alphas[n][0] * self.betas[n][0])
                numA, denA = self.reestimate_A_scaled(n)
                num_A += numA
                den_A += denA
                numB, denB = self.reestimate_B_scaled(n)
                num_B += numB
                den_B += denB
                self.costs.append(np.sum(self.logP.copy()))

            self.pi = pi / self.N
            self.A = num_A / den_A
            self.B = num_B / den_B

    

    def likelihood(self, x):
        r"""Compute likelihood P(x/lambda) given an observed sequence x.
1
        Arguments :
            x -- the observed sequence
        """ 

        T = len(x)
        alpha = np.zeros((T, self.M))
        alpha[0] = self.pi*self.B[:, x[0]]
        for t in range(1, T):
            alpha[t] = alpha[t-1].dot(self.A) * self.B[:, x[t]]
        return alpha[-1].sum()

    def log_likelihood(self, x):
        r"""Compute log likelihood log(P(x/lambda)) given an observed sequence x.
1
        Arguments :
            x -- the observed sequence
        """ 

        T = len(x)
        scale = np.zeros(T)
        alpha = np.zeros((T, self.M))
        alpha[0] = self.pi*self.B[:, x[0]]
        for t in range(1, T):
            alpha_t = alpha[t-1].dot(self.A) * self.B[:, x[t]]
            scale[t] = alpha_t.sum()
            alpha[t] = alpha_t / scale[t]
        return np.log(scale[-1].sum())

    def log_likelihood_multi(self, X):
        r"""Compute log likelihoods log(P(x/lambda)) given observed sequence x
        of vector X .
1
        Arguments :
            X -- the observed sequences vector
        """ 
        return np.array([self.log_likelihood(x) for x in X])

    def get_state_sequence(self, x):
        r"""Compute Viterbi algorithm in order to get the optimal state sequence .
1
        Arguments :
            x -- the observed sequences 
        """ 
        
        T = len(x)
        delta = np.zeros((T, self.M))
        psi = np.zeros((T, self.M))
        delta[0] = self.pi*self.B[:, x[0]]

        for t in range(1, T):
            for j in range(self.M):
                delta[t, j] = np.max(delta[t-1]*self.A[:, j]) * self.B[j, x[t]]
                psi[t, j] = np.argmax(delta[t-1]*self.A[:, j])

        # finding the path
        states = np.zeros(T, dtype=np.int32)
        states[T-1] = np.argmax(delta[T-1])
        for t in reversed(range(T-1)):
            states[t] = psi[t+1, states[t+1]]
        return states

    def get_state_sequence_scaled(self, x):
        r"""Compute Viterbi algorithm in order to get the optimal state sequence .
1
        Arguments :
            x -- the observed sequences 
        """ 

        T = len(x)
        delta = np.zeros((T, self.M))
        psi = np.zeros((T, self.M))
        delta[0] = np.log(self.pi) + np.log(self.B[:, x[0]])

        for t in range(1, T):
            for j in range(self.M):
                delta[t, j] = np.max(
                    delta[t-1] + np.log(self.A[:, j])) * np.log(self.B[j, x[t]])
                psi[t, j] = np.argmax(delta[t-1] + np.log(self.A[:, j]))

        # finding the path
        states = np.zeros(T, dtype=np.int32)
        states[T-1] = np.argmax(delta[T-1])
        for t in reversed(range(T-1)):
            states[t] = psi[t+1, states[t+1]]
        return states
