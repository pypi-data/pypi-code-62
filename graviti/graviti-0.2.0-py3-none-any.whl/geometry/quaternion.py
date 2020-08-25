#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Quaternion."""

import collections
from typing import Dict, Optional, Sequence, Union

import numpy as np
import pyquaternion


class Quaternion(pyquaternion.Quaternion):  # type: ignore[misc]
    """Class to represent a 4-dimensional complex number or quaternion.

    Quaternion objects can be used generically as 4D numbers,
    or as unit quaternions to represent rotations in 3D space.

    It is an encapsulation of `pyquaternion.Quaternion`
    See Object Initialisation docs for complete behaviour:

    http://kieranwynn.github.io/pyquaternion/initialisation/

    What difference:
    1. keyword-only argument: "loads"
        >>> Quaternion(loads={"w": 1, "x": 0, "y": 0, "z": 0})
        >>> Quaternion(1.0, 0.0, 0.0, 0.0)

    2. Possible to init from a 3*3 List
        >>> Quaternion([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        >>> Quaternion(1.0, 0.0, 0.0, 0.0)

    3. Possible to init from None
        >>> Quaternion(None)
        >>> Quaternion(1.0, 0.0, 0.0, 0.0)

    :param args: Coordinates of the Quaternion
    :param loads: A dicitionary containing coordinates of a Quaternion
    :param kwargs: keyword-only argument to the Quaternion
    """

    ArgsType = Union[
        None, Sequence[float], Sequence[Sequence[float]], np.ndarray, pyquaternion.Quaternion
    ]
    KwargsType = Union[None, float, Sequence[float], np.ndarray]

    def __init__(
        self,
        *args: Union[ArgsType, float],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: KwargsType
    ) -> None:
        if loads:
            super().__init__(**loads)
            return

        if len(args) == 1:
            arg = args[0]
            if arg is None:
                super().__init__()
                return

            if isinstance(arg, collections.abc.Sequence):
                arg = np.array(arg, dtype=np.float64)

            if isinstance(arg, np.ndarray):
                if arg.shape == (3, 3) or arg.shape == (4, 4):
                    super().__init__(matrix=arg)
                    return

        super().__init__(*args, **kwargs)

    def dumps(self) -> Dict[str, float]:
        """Dumps the Quaternion as a dictionary.

        :return: A dictionary containing Quaternion information
        """
        return {"w": self.w, "x": self.x, "y": self.y, "z": self.z}
