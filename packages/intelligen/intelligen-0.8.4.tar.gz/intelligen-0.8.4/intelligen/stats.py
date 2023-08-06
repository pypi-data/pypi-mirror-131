import numpy as np
import matplotlib.pyplot as plt
from math import factorial
from typing import List
Vector = List[float]

def combination(n: int, k: int) -> int:
    """Return the number of combinations for a set of n items in k selected items

    Args:
        n (int): total number of items
        k (int): selected number of items

    Returns:
        int: number of combinations
    """
    return factorial(n) / (factorial(k)*factorial(n-k))

def mean_squared_error(y_real: Vector, y_pred: Vector) -> float:
    """Returns the mean squared error

    Args:
        y_real (Vector): Real data
        y_pred (Vector): Predicted data

    Returns:
        float: mean squared error
    """
    y_real = np.array(y_real)
    y_pred = np.array(y_pred)
    
    return np.mean((y_real - y_pred)**2)

def mean_absolute_error(y_real: Vector, y_pred: Vector) -> float:
    """Returns the mean absolute error

    Args:
        y_real (Vector): Real data
        y_pred (Vector): Predicted data

    Returns:
        float: mean absolute error
    """
    y_real = np.array(y_real)
    y_pred = np.array(y_pred)
    
    return np.mean(np.abs(y_real - y_pred))

def expectation(x: Vector, p: Vector = None) -> float:
    """Returns the expected value

    Args:
        x (Vector): Values
        p (Vector, optional): Probability. Defaults to None.

    Returns:
        float: Expectation
    """
    x = np.array(x)
    if p is None: p = (1/len(x)) * np.ones([1,len(x)]) 
    else: np.array(p)
    return np.sum(x*p)
    
def variance(x: Vector, p: Vector = None) -> float:
    """Return the dispersion of the values

    Args:
        x (Vector): Values
        p (Vector, optional): Probability. Defaults to None.

    Returns:
        float: Variance
    """
    x = np.array(x)
    if p is None: p = (1/len(x)) * np.ones([1,len(x)])
    else: np.array(p) 
    return np.sum((x - np.mean(x))**2) / len(x)
    #Second option
    #return expectation(x**2,p) - expectation(x,p)**2

def standard_deviation(x: Vector, p: Vector = None) -> float:
    """Returns the standard deviation

    Args:
        x (Vector): Values
        p (Vector, optional): Probability. Defaults to None.

    Returns:
        float: Standard deviation
    """
    return np.sqrt(variance(x,p))

class Distribution:
    
    def __init__(self) -> None:
        pass

    def plot_PMF(self, show = True) -> None:
        plt.title(f'Probability mass function\n{self.__class__.__name__}')
        data = []
        for i in range(self.plot + 1):
            data.append(self.PMF(i))
        plt.plot(data)
        if show: plt.show()
    
    def plot_CDF(self, show = True) -> None:
        plt.title(f'Cumulative distribution function\n{self.__class__.__name__}')
        data = []
        for i in range(self.plot + 1):
            data.append(self.CDF(i))
        plt.step(range(len(data)), data, where='post')
        if show: plt.show()
    
    def plot_PDF(self, show = True) -> None:
        plt.title(f'Probability density function\n{self.__class__.__name__}')
        data = []
        iter = np.linspace(-self.plot + self.origin, self.plot + self.origin, 1000)
        for i in iter:
            data.append(self.PDF(i))
        plt.plot(iter, data)
        if show: plt.show()

class Binomial(Distribution):

    def __init__(self, n: int, p: float) -> None:
        self.n, self.p, self.plot = n, p, n
    
    def PMF(self, k: int) -> float:
        """Returns the probability mass function P(x=k)

        Args:
            k (float): Value

        Returns:
            float: Probability
        """
        return combination(self.n, k) * self.p**k * (1 - self.p)**(self.n - k) 

    def CDF(self, k: float):
        result = 0
        for i in range(int(np.floor(k))+1):
            result += combination(self.n, i) * self.p**i * (1 - self.p)**(self.n - i)
        return result

class Geometric(Distribution):
    
    def __init__(self, p: float, plot: int = None) -> None:
        self.p = p
        if plot is None: self.plot = int(10/p)

    def PMF(self, k: int) -> float:
        return (1 - self.p)**(k - 1) * self.p
    
    def CDF(self, k: int) -> float:
        return 1 - (1 - self.p)**k

class Hypergeometric(Distribution):
    
    def __init__(self, N: int, n: int, r: int) -> None:
        self.N, self.n, self.r, self.plot = N, n, r, r

    def PMF(self, k: int) -> float:
        return combination(self.r, k) * combination(self.N - self.r, self.n - k) / combination(self.N, self.n)


class Poisson(Distribution):

    def __init__(self, l: float, plot: float = None) -> None:
        self.l = l
        if plot is None: self.plot = int(l*2) + 5
    
    def PMF(self, k: int) -> float:
        return np.exp(-self.l) * self.l**k / factorial(k)

class Normal(Distribution):

    def __init__(self, mu: float = 0, s: float = 1) -> None:
        self.mu, self.s, self.plot, self.origin = mu, s, 3*(s+1), mu
    
    def PDF(self, k: float) -> float:
        return np.exp((-1/2) * ((k - self.mu)/self.s)**2) / (self.s * np.sqrt(2*np.pi)) 
