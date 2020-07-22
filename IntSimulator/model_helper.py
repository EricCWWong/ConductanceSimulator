import numpy as np


def get_array(array_range, steps, reverse=False):
    """
        This helper function helps us generate an array given a range
        and number of steps.

    Parameters
    ----------
    array_range: tuple (float, float)
        This is the range of the concerned array. The lower bound first.
    steps: int
        This is the number of steps we want from the generated array.
    reverse: bool (Optional)
        This indicates whether we want to reverse the array. Default is
        True.

    Returns
    -------
    output: numpy array
        After receiving the array range and number of steps, a numpy
        array is generated.
    """

    if array_range[1] == array_range[0]:
        return np.full(steps, array_range[1])
    else:
        step_size = (array_range[1] - array_range[0]) / steps

        output = np.arange(start=array_range[0],
                           stop=array_range[1],
                           step=step_size)

        if reverse is True:
            output = output[::-1]
        return output
