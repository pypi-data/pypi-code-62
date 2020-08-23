import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial cs_probdist class for calculating and
    visualizing a Binomial cs_probdist.
    
    Attributes:
        mean (float) representing the mean value of the cs_probdist
        stdev (float) representing the standard deviation of the cs_probdist
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
    
    
    TODO: Fill out all TODOs in the functions below
            
    """
    
    #       A binomial cs_probdist is defined by two variables:
    #           the probability of getting a positive outcome
    #           the number of trials
    
    #       If you know these two values, you can calculate the mean and the standard deviation
    #       
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))
    
    #       
    
    def __init__(self, prob=.5, size=20):

        Distribution.__init__(self)
        self.p = prob
        self.n = size

    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """

        self.mean = self.p * self.n

        return self.mean



    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))

        return self.stdev
        
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """

        self.n = len(self.data)
        self.p = sum(self.data) / self.n
        self.calculate_mean()
        self.calculate_stdev()

        return self.p, self.n


    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        plt.bar(x = ['0', '1'], height = [(1 - self.p) * self.n, self.p * self.n])
        plt.xlabel('Data')
        plt.ylabel('Frequency')
        plt.title('Bar Chart of Data')
        plt.show()


    def pdf(self, k):
        """Probability density function calculator for the gaussian cs_probdist.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        comb = math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k))

        return comb * (self.p ** k) * ((1 - self.p) ** (self.n - k))


    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial cs_probdist
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
    
        # TODO: Use a bar chart to plot the probability density function from
        # k = 0 to k = n
        
        #   Hint: You'll need to use the pdf() method defined above to calculate the
        #   density function for every value of k.
        
        #   Be sure to label the bar chart with a title, x label and y label

        #   This method should also return the x and y values used to make the chart
        #   The x and y values should be stored in separate lists

        x = []
        y = []

        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        plt.bar(x, y)
        plt.xlabel("# of Success")
        plt.ylabel("Probability")
        plt.title("Probability Distribution of Binomial Data")
        plt.show()


    def __add__(self, other):
        
        """Function to add together two Binomial cs_probdist with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial cs_probdist
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        result = Binomial(self.p, self.n + other.n)
        result.calculate_mean()
        result.calculate_stdev()

        return result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """

        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
