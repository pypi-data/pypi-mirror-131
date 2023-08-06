from typing import Callable, List
Vector = List[float]

import numpy as np

def lagrange(X: Vector, Y: Vector) -> Callable[[Vector], Vector]:
    """Returns the lagrange interpolation
    Args:
        X (Vector): X-data
        Y (Vector): Y-data
    Returns:
        Callable[[Vector], Vector]: returns the function that evaluates the lagrange interpolation
    """
    if type(X) == list:
        X = np.array(X)  

    def lagran(x):
        # Checks the input's type
        if type(x) == 'numpy.ndarray':
            x = x.reshape(-1, 1)
        
        if type(x) == list:
            x = np.array(x).reshape(-1, 1)
        
        else:
            x = np.array([x]).reshape(-1, 1)

        out = 0
        for i in range(len(X)):
            #pi_x = (x - np.array([(X[X != xi]).reshape(-1)] * len(x))) because X[X != xi] autoreshape (-1)
            pi_x = x - np.array([(X[X != X[i]])] * len(x))

            out += Y[i] * (pi_x / (X[i] - X[X != X[i]])).prod(axis = 1)

        return out
    
    return lagran


def main() -> None:
    X = np.array([-1, 0, 4,  1, 7, 8])
    X = np.concatenate((X, X+10))
    Y = np.array([ 4, 2, 3, -2, 6, 6])
    Y = np.concatenate((Y, Y+1))

    _x = np.linspace(min(X),max(X),1000)


    Lagran = lagrange(X.reshape(-1, 1),Y.reshape(-1, 1))
    
    #Lagran = lagrange(X,Y)
    
    plt.scatter(X, Y, c='salmon')
    plt.plot(_x, Lagran(_x))
    plt.show()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    main()