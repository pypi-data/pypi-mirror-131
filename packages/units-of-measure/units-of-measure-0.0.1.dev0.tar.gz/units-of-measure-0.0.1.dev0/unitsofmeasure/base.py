from unitsofmeasure import Dimension, Unit, UnitClass

class SiBaseUnits(UnitClass):
    """SI Base Units"""
    kg  = Unit(Dimension(kg=1),3,"kg","kilogram")
    m   = Unit(Dimension(m=1),0,"m","meter")
    s   = Unit(Dimension(s=1),0,"s","second")
    A   = Unit(Dimension(A=1),0,"A","ampere")
    K   = Unit(Dimension(K=1),0,"K","kelvin")
    cd  = Unit(Dimension(cd=1),0,"cd","candela")
    mol = Unit(Dimension(mol=1),0,"mol","mol")

    @classmethod
    def get_units(cls) -> dict[str, Unit]:
        return {
            "kg":  cls.kg,
            "m":   cls.m,
            "s":   cls.s,
            "A":   cls.A,
            "K":   cls.K,
            "cd":  cls.cd,
            "mol": cls.mol
        }
