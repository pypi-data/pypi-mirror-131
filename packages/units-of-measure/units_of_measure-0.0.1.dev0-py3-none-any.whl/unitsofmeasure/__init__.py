"""Units of Measure

Classes

  Dimension: Linear combination of SI base units
  Unit: Dimension mapped to a symbol and a name
  UnitMap: Map objects to units
"""

class Dimension:
    """Dimension of quantity as defined in the International System of Units - 9th edition

    A linear combination of SI base units.
    See https://www.bipm.org/en/publications/si-brochure
    """

    def __init__(
            self,
            kg:  int = 0,
            m:   int = 0,
            s:   int = 0,
            A:   int = 0,
            K:   int = 0,
            cd:  int = 0,
            mol: int = 0
        ):
        self.kg  = kg
        self.m   = m
        self.s   = s
        self.A   = A
        self.K   = K
        self.cd  = cd
        self.mol = mol
    
    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return (
            self.kg  == other.kg and
            self.m   == other.m  and
            self.s   == other.s  and
            self.A   == other.A  and
            self.K   == other.K  and
            self.cd  == other.cd and
            self.mol == other.mol
        )


class Unit:
    """A Unit has a Dimension.

    Scalars are the null vector, which is the default dimension.
    Units have a prefix, which specifies the order of magnitude in base 10.
    Prefixes that are integer multiples of 3 in the interval [-24,24] map to SI prefixes.
    Units have a symbol: a short string used in formulas, tables, and charts.
    """
    
    def __init__(
            self,
            dimension: Dimension = Dimension(), # scalar
            prefix: int = 0,
            symbol: str = "",
            name: str = ""
        ):
        self.dimension = dimension
        self.prefix = prefix
        self.symbol = symbol
        self.name = name
    
    def __str__(self):
        return self.symbol

class UnitMap:
    """Map objects to their units.

    The objects are not used as keys directly, because not all objects are hashable.
    Instead the integer value of id(object) is used as key,
    but two objects with non-overlapping lifetimes may have the same id() value.
    See https://docs.python.org/3/library/functions.html#id.
    The units can be objects as well and need not be of type Unit.
    """

    def __init__(self):
        self.units = {} # dictionary maps id(object) to (object, unit)
    
    def map_to_unit(self, o: object, unit: object):
        """Map the object ID to the tuple (object, unit) to keep a reference to the object.

        Otherwise the object could be garbage collected and its ID re-used for a different object.
        TODO Use weak references for objects and remove the object ID from the dictionary on finalize.
        """
        
        self.units[id(o)] = (o, unit)

    def get_unit_of(self, o: object) -> object:
        """Return the unit mapped to the object."""

        # map the object ID to its tuple (object, unit) and then return the unit
        return self.units[id(o)][1]

class UnitClass:
    """Dictionary of Units"""

    unit_map: dict[str, Unit] = {}

    @classmethod
    def get_units(cls) -> dict[str, Unit]:
        return cls.unit_map
