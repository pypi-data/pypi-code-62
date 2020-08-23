from simframe.integration.scheme import Scheme

# Butcher coefficients
a10 = 0.5
c1 = 0.5


def _f_expl_2_midpoint(x0, Y0, dx, *args, **kwargs):
    """Explicit 2nd-order midpoint method

    Parameters
    ----------
    x0 : Intvar
        Integration variable at beginning of scheme
    Y0 : Field
        Variable to be integrated at the beginning of scheme
    dx : IntVar
        Stepsize of integration variable
    args : additional positional arguments
    kwargs : additional keyworda arguments

    Returns
    -------
    Y1 : Field
        New value of Y

    Butcher tableau
    ---------------
      0  |  0   0
     1/2 | 1/2  0
    -----|---------
         |  0   1
    """
    k0 = Y0.derivative(x0, Y0)
    k1 = Y0.derivative(x0 + c1*dx, Y0 + a10*k0*dx)

    return Y0 + dx*k1


expl_2_midpoint = Scheme(
    _f_expl_2_midpoint, description="Explicit 2nd-order midpoint method")
