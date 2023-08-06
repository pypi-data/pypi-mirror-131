import numpy as np
from typing import Callable, List
Function = Callable[[float], float]

def newton(f: Function, df: Function, x: float, tol: float, iter: bool = False) -> float:
    """Newton method to find a root of a function
    Args:
        f (Function): Function
        df (Function): Derivate of the function
        x (float): Start point
        tol (float): Error tolerance
        iter (bool, optional): Shows the iterations needed to find the solution. Defaults to False.
    Returns:
        float: The root
        int: Number of iterations (optional)
    """
    n = 0
    while abs(f(x)) > tol:
        x = x - f(x) / df(x)
        n += 1

    if iter:
        return x, n
    return x

def bisection(f: Function, xi: float, xf: float, tol: float, iter: bool = False) -> float:
    """Bisection method to find a root of a function
    Args:
        f (Function): Function
        xi (float): First point
        xf (float): Second point
        tol (float): Error tolerance
        iter (bool, optional): Shows the iterations needed to find the solution. Defaults to False.
    Returns:
        float: The root
        int: Number of iterations (optional)
    """
    if f(xi) * f(xf) < 0:
        xm, n = (xi + xf) / 2, 1

        while abs(f(xm)) > tol:
            if f(xi) * f(xm) < 0:
                xf = xm 
                n += 1
            
            elif f(xm) * f(xf) < 0:
                xi = xm 
                n += 1
            
            xm = (xi + xf) / 2
            
        if iter:
            return xm, n
        return xm

    else:
        print("Invalid input")

def regula_falsi(f: Function, xi: float, xf: float, tol: float, iter: bool = False) -> float:
    """Regula falsi method to find a root of a function
    Args:
        f (Function): Function
        xi (float): First point
        xf (float): Second point
        tol (float): Error tolerance
        iter (bool, optional): Shows the iterations needed to find the solution. Defaults to False.
    Returns:
        float: The root
        int: Number of iterations (optional)
    """
    if f(xi) * f(xf) < 0:
        xm, n = (xi * f(xf) - xf * f(xi)) / (f(xf) - f(xi)), 1

        while abs(f(xm)) > tol:
            if f(xi) * f(xm) < 0:
                xf = xm
                n += 1

            if f(xm) * f(xf) < 0:
                xi = xm
                n += 1
            
            xm = (xi * f(xf) - xf * f(xi)) / (f(xf) - f(xi))

        if iter:
            return xm, n
        return xm
    else:
        print("Invalid input")


def secant(f: Function, x0: float, x1: float, tol: float, iter: bool = False) -> float:
    """Secant method to find a root of a function
    Args:
        f (Function): Function
        x0 (float): First point
        x1 (float): Second point
        tol (float): Error tolerance
        iter (bool, optional): Shows the iterations needed to find the solution. Defaults to False.
    Returns:
        float: The root
        int: Number of iterations (optional)
    """    
    x2, n = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0)), 1

    while abs(f(x2)) > tol:
        x0, x1 = x1, x2
        x2 = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))
        n += 1
        
    if iter:
        return x2, n
    return x2



""" def fixed_point(g, dg, x, tol, iter = False):
  ''' f(x) = 0 ==> x = g(x) '''
  n = 1
  if abs(dg(x))<1:
    xa = x
    x = g(x)
    
    while abs(x-xa)>tol:
      xa = x
      x = g(x)
      n = n+1
    if iter: return x, n
    return x
  else:
    print("Doesn't converge")  """


def newton2(f: Function, df: Function, ddf: Function, x: float, tol: float, iter: bool = False) -> float:
    """Newton second order method to find a root of a function
    Args:
        f (Function): Function
        df (Function): Derivate of the function
        ddf (Function): Second derivate of the function
        x (float): Start point
        tol (float): Error tolerance
        iter (bool, optional): Shows the iterations needed to find the solution. Defaults to False.
    Returns:
        float: The root
        int: Number of iterations (optional)
    """
    n = 0

    while abs(f(x)) > tol:
        x1 = x - df(x) / ddf(x) + np.sqrt(df(x)**2 - 2*ddf(x) * f(x)) / ddf(x)
        x2 = x - df(x) / ddf(x) - np.sqrt(df(x)**2 - 2*ddf(x) * f(x)) / ddf(x)

        if abs(f(x1)) < abs(f(x2)):
            x = x1
        else:
            x = x2
        
        n += 1
    
    if iter:
        return x, n
    return x


def main() -> None:
    def f(x): return x**3 + 2*x**2 + 10*x - 20
    def df(x): return 3*x**2 + 4*x + 10
    def ddf(x): return 6*x + 4

    def g(x): return (-x**3 - 2*x**2 + 20) / 10
    def dg(x): return (-3*x**2 - 4*x) / 10

    print('Newton:      ', newton(f, df, 1, 0.01, True))
    print('Bisection:   ', bisection(f, 1, 2, 0.01, True))
    print('Regula falsi:', regula_falsi(f, 1, 2, 0.01, True))
    print('Secant:      ', secant(f, 1, 2, 0.01, True))
    #print(fixed_point(g, dg, 0, 0.1, True))
    print('Newton 2     ', newton2(f, df, ddf, 1, 0.01, True))



if __name__ == '__main__':
    main()