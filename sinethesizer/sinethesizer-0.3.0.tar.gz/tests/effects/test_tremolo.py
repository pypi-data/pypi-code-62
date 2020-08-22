"""
Test `sinethesizer.effects.tremolo` module.

Author: Nikolay Lysenko
"""


from typing import Any, Dict

import numpy as np
import pytest

from sinethesizer.effects.tremolo import apply_tremolo


@pytest.mark.parametrize(
    "sound, frame_rate, sound_frequency, kind, kwargs, expected",
    [
        (
            # `sound`
            np.vstack((
                np.arange(12, dtype=float),
                np.arange(12, dtype=float)
            )),
            # `frame_rate`
            12,
            # `sound_frequency`
            None,
            # `kind`
            'absolute',
            # `kwargs`
            {'frequency': 3, 'amplitude': 0.25},
            np.array([
                [0, 1.25, 2, 2.25, 4, 6.25, 6, 5.25, 8, 11.25, 10, 8.25],
                [0, 1.25, 2, 2.25, 4, 6.25, 6, 5.25, 8, 11.25, 10, 8.25]
            ])
        ),
        (
            # `sound`
            np.vstack((
                    np.arange(12, dtype=float),
                    np.arange(12, dtype=float)
            )),
            # `frame_rate`
            12,
            # `sound_frequency`
            1,
            # `kind`
            'relative',
            # `kwargs`
            {'frequency_ratio': 3, 'amplitude': 0.25},
            np.array([
                [0, 1.25, 2, 2.25, 4, 6.25, 6, 5.25, 8, 11.25, 10, 8.25],
                [0, 1.25, 2, 2.25, 4, 6.25, 6, 5.25, 8, 11.25, 10, 8.25]
            ])
        ),
    ]
)
def test_apply_tremolo(
        sound: np.ndarray, frame_rate: int, sound_frequency: float, kind: str,
        kwargs: Dict[str, Any], expected: np.ndarray
) -> None:
    """Test `apply_tremolo` function."""
    sound_info = {
        'frame_rate': frame_rate,
        'fundamental_frequency': sound_frequency
    }
    result = apply_tremolo(sound, sound_info, kind, **kwargs)
    np.testing.assert_almost_equal(result, expected)
