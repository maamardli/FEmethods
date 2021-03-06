"""
Base module that contains base classes to be used by other modules
"""


class Validator(object):
    """Decorator class used to validate parameters"""

    @staticmethod
    def positive(param_name="parameter"):
        """Function decorator to handle validating input parameters to ensure
        parameters are positive values.

        The input, param_name, is the parameter name that will show up in the
        call-stack when an invalid parameter is entered.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                if type(args[1]) not in (int, float):
                    raise TypeError(param_name + " must be a positive number!")
                if args[1] <= 0:
                    raise ValueError(param_name + " must be positive!")
                func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def non_negative(param_name="parameter"):
        """Function decorator to handle validating input parameters to ensure
        parameters are non-negative (positive or zero values).

        The input, param_name, is the parameter name that will show up in the
        call-stack when an invalid parameter is entered.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                if type(args[1]) not in (int, float):
                    raise TypeError(param_name + " must be a positive number!")
                if args[1] < 0:
                    raise ValueError(param_name + " must be non-negative!")
                func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def islist(param_name="parameter"):
        """Function decorator to handle validating input parameters to ensure
        parameters are a list.

        The input, param_name, is the parameter name that will show up in the
        call-stack when an invalid parameter is entered.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                if not isinstance(args[1], list):
                    raise TypeError(param_name + " must be a list!")
                func(*args, **kwargs)

            return wrapper

        return decorator


class Forces(object):
    """Base class for all loads and reactions"""

    def __init__(self, magnitude, location=0):
        self.magnitude = magnitude
        self.location = location

    @property
    def magnitude(self):
        return self._magnitude

    #
    @magnitude.setter
    def magnitude(self, magnitude):
        if not isinstance(magnitude, (int, float, type(None))):
            raise TypeError("force value must be a number")
        self._magnitude = magnitude

    @property
    def location(self):
        return self._location

    @location.setter
    @Validator.non_negative("location")
    def location(self, location):
        self._location = location

    def __repr__(self):
        return (
                f"{self.__class__.__name__}(magnitude={self.magnitude}, "
                + f"location={self.location})"
        )

    def __add__(self, force2):
        f1 = self.magnitude
        x1 = self.location

        f2 = force2.magnitude
        x2 = force2.location

        x = (f1 * x1 + f2 * x2) / (f1 + f2)
        return self.__class__(f1 + f2, x)

    def __eq__(self, other):
        return self.magnitude * self.location == other.magnitude * other.location  # noqa: E501

    def __sub__(self, force2):
        f1 = self.magnitude
        x1 = self.location

        f2 = force2.magnitude
        x2 = force2.location

        x = (f1 * x1 - f2 * x2) / (f1 - f2)
        return self.__class__(f1 - f2, x)


def derivative(func, x0, n=1, method="forward"):  # pragma: no cover
    """
    Calculate the nth derivative of function f at x0

     Calculate the 1st or 2nd order derivative of a function using
     the forward or backward method.
    """

    if n not in (1, 2):
        raise ValueError("n must be 1 or 2")

    # Note that the value for dx is set manually. This is because the ideal
    # values are not constant based on the method used.
    # TODO determine better method for choosing a more ideal dx value
    if method == "forward":
        dx = 1e-8
        if n == 1:
            return (func(x0 + dx) - func(x0)) / dx
        elif n == 2:
            return (func(x0 + 2 * dx) - 2 * func(x0 + dx) + func(x0)) / dx ** 2
    elif method == "backward":
        dx = 1e-5
        if n == 1:
            return (func(x0) - func(x0 - dx)) / dx
        elif n == 2:
            return (func(x0) - 2 * func(x0 - dx) + func(x0 - 2 * dx)) / dx ** 2
    else:
        raise ValueError(f'invalid method parameter "{method}"')
