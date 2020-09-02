
import sys
sys.path.append(sys.path[0]+'/../../strlib')

from section.section_material import ReinforcedConcrete, Mixte, Steel, Timber


class TestReinforcedConcrete:

    @classmethod
    def setup_class(cls):
        print("Avant mon teste unitaire", cls)

    @classmethod
    def teardown_class(cls):
        print("après mon test unitaire", cls)
    
    def test_nothing(self):
        """ """
        raise NotImplementedError
