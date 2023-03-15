import unittest

from jarvis_calc.database_interactors.db_controller import DBController

from jarvis_factory.factories.jcalc import JCalcClassesFactory


class FactoriesTest(unittest.TestCase):
    def test_singleton_db_controller(self):
        controller1: DBController = JCalcClassesFactory.create_db_controller()
        controller2: DBController = JCalcClassesFactory.create_db_controller()

        self.assertEqual(controller1, controller2)


if __name__ == '__main__':
    unittest.main()
