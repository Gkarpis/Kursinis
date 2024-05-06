import unittest
from unittest.mock import patch
import sys

# Ensure the MotoDash module is accessible, adjust the path as needed.
sys.path.append(r'C:\Users\lopas\Documents\vsstd\Python\Kurs')

# Attempt to import the necessary components from your module.
try:
    from MotoDash import SuzukiGSX, HondaCBR, HondaHornet, motorcycle_factory, MotorcycleDashboard, save_state, load_state
except ImportError as e:
    print(f"Failed to import modules due to: {e}")
    sys.exit(1)

class TestMotorcycleFunctions(unittest.TestCase):
    def setUp(self):
        # Initialize instances for each motorcycle type
        self.bike_suzuki = SuzukiGSX()
        self.bike_honda_cbr = HondaCBR()
        self.bike_honda_hornet = HondaHornet()

    def test_acceleration(self):
        # Verify that acceleration increases speed
        speed_before = self.bike_suzuki.speed
        self.bike_suzuki.accelerate()
        self.assertGreater(self.bike_suzuki.speed, speed_before, "Acceleration should increase speed.")

    def test_braking(self):
        # Verify that braking decreases speed
        self.bike_honda_cbr.speed = 30  # Set initial speed
        self.bike_honda_cbr.brake()
        self.assertLess(self.bike_honda_cbr.speed, 30, "Braking should reduce speed.")

    def test_gear_change_on_acceleration(self):
        # Verify that gears change correctly on acceleration
        self.bike_honda_hornet.speed = 60  # Set speed to trigger gear change
        self.bike_honda_hornet.accelerate()
        self.assertEqual(self.bike_honda_hornet.gear, 2, "Gear should change to 2 at speed 60")

    def test_gear_change_on_braking(self):
        # Verify that gears change correctly when braking
        self.bike_honda_cbr.speed = 65
        self.bike_honda_cbr.gear = 3
        self.bike_honda_cbr.brake()
        self.bike_honda_cbr.brake()  # Ensure speed drops sufficiently
        self.assertEqual(self.bike_honda_cbr.gear, 2, "Gear should downshift to 2 when speed drops below 60")

    def test_cruise_control(self):
        # Verify cruise control functionality sets the correct speed
        self.bike_suzuki.toggle_cruise_control()
        self.assertEqual(self.bike_suzuki.speed, 50, "Cruise control should set speed to 50")

    @patch('MotoDash.save_state')
    def test_save_state(self, mock_save_state):
        # Test the save state functionality by ensuring no exception is raised
        save_state(self.bike_honda_cbr)
        mock_save_state.assert_called_once_with(self.bike_honda_cbr)

    @patch('MotoDash.load_state')
    def test_load_state(self, mock_load_state):
        # Setup the mock to return a specific object
        mock_load_state.return_value = self.bike_honda_cbr
        motorcycle = load_state()
        self.assertIsNotNone(motorcycle, "Loaded motorcycle should not be None")
        self.assertTrue(hasattr(motorcycle, 'accelerate'), "Loaded object should have an accelerate method")
        mock_load_state.assert_called_once()

# Execute the tests
if __name__ == '__main__':
    unittest.main(exit=False)
