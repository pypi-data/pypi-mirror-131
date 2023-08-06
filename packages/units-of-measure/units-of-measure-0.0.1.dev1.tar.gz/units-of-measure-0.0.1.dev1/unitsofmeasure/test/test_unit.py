"""Test Unit"""
import pytest
from unitsofmeasure import Dimension, Unit

@pytest.mark.parametrize(
    "dimension        , prefix , symbol , name"     ,[
    (Dimension()      ,      0 , "%"    , "percent" ), # scalar
    (Dimension(kg=1)  ,      3 , "kg"   , "kilogram"), # SI base units
    (Dimension(m=1)   ,      0 , "m"    , "meter"   ),
    (Dimension(s=1)   ,      0 , "s"    , "second"  ),
    (Dimension(A=1)   ,      0 , "A"    , "ampere"  ),
    (Dimension(K=1)   ,      0 , "K"    , "kelvin"  ),
    (Dimension(cd=1)  ,      0 , "cd"   , "candela" ),
    (Dimension(mol=1) ,      0 , "mol"  , "mol"     )
])
def test_unit(dimension: Dimension, prefix: int, symbol: str, name: str):
    unit = Unit(dimension=dimension, prefix=prefix, symbol=symbol, name=name)
    assert unit.dimension == dimension
    assert unit.prefix    == prefix
    assert unit.symbol    == symbol
    assert unit.name      == name
