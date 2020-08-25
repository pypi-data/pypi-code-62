from tank_forecaster import decomp, validation

def test_decomp_tank(tank_full_data):
    val = validation.format_tank(tank_full_data)
    x = decomp.decompose_tank(val)
    assert len(x) == 48
