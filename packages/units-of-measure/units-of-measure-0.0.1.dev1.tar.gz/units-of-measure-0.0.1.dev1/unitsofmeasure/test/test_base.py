from unitsofmeasure.base import SiBaseUnits

def test_it():
    for (key, unit) in SiBaseUnits.get_units().items():
        assert key == unit.symbol
