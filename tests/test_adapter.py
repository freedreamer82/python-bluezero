"""
Tests for the Adapter.

This test class makes use of sample DBus data captured from a live device,
imported as ``tests.obj_data``.
"""
import os
import subprocess
import sys
from time import sleep
import unittest
from bluezero import adapter


class TestBluezeroAdapter(unittest.TestCase):
    """
    Mock a BLE Adapter.
    """

    def setUp(self):
        """
        running using the emulator/btvirt to create virtual Bluetooth devices
        """
        self.dut_uuid = '00:AA:01:00:00:23'

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.p = subprocess.Popen(['sudo',
                                   '{}/emulator/btvirt'.format(dir_path),
                                   '-l2'], preexec_fn=os.setpgrp)
        # Wait for the service to become available
        sleep(0.01)
        self.dongle = adapter.Adapter(self.dut_uuid)

    def tearDown(self):
        """
        Stop the module patching.
        """
        subprocess.run(["sudo", "kill", str(self.p.pid)])

    def test_list_adapters(self):
        """
        Test ``Adapter.list_adapters()``
        """
        adapters = adapter.list_adapters()
        self.assertIn(self.dut_uuid, adapters)

    def test_get_all(self):
        """
        Test the ``get_all()`` method for retrieving all the DBus properties.
        """
        some_values = {'Address': '00:AA:01:00:00:23',
                       'Class': 786700,
                       'Discoverable': False,
                       'DiscoverableTimeout': 180,
                       'Discovering': False,
                       'Pairable': True,
                       'PairableTimeout': 0,
                       'Powered': True,
                       'UUIDs': ['00001112-0000-1000-8000-00805f9b34fb',
                                 '0000110a-0000-1000-8000-00805f9b34fb',
                                 '00001200-0000-1000-8000-00805f9b34fb',
                                 '0000110e-0000-1000-8000-00805f9b34fb',
                                 '00001108-0000-1000-8000-00805f9b34fb',
                                 '0000110c-0000-1000-8000-00805f9b34fb',
                                 '00001800-0000-1000-8000-00805f9b34fb',
                                 '00001801-0000-1000-8000-00805f9b34fb',
                                 '0000110b-0000-1000-8000-00805f9b34fb']
                       }
        for i in some_values:
            with self.subTest(i=i):
                self.assertIn(i, list(self.dongle.get_all().keys()))

    def test_adapter_address(self):
        """
        Test the adapter ``address`` property.
        """
        self.assertEqual(self.dongle.address, self.dut_uuid)

    def test_adapter_name(self):
        """
        Test the adapter ``name`` property.
        """
        self.assertIsInstance(self.dongle.name, str)

    def test_adapter_alias(self):
        """
        Test the adapter ``alias`` property.
        """
        self.assertIsInstance(self.dongle.alias, str)

    def test_adapter_alias_write(self):
        """
        Test that an adapter ``alias`` can be set.
        """
        dev_name = 'my-test-dev'
        # test
        self.dongle.alias = dev_name
        self.assertEqual(dev_name, self.dongle.alias)

    def test_class(self):
        """
        Test the adapter ``bt_class`` property.
        """
        # test
        self.assertEqual(0, self.dongle.bt_class)

    def test_adapter_power(self):
        """
        Test the adapter ``powered`` property.
        """
        self.assertEqual(1, self.dongle.powered)

    def test_adapter_power_write(self):
        """
        Test that the adapter ``powered`` property can be set.
        """
        self.dongle.powered = False
        self.assertEqual(False, self.dongle.powered)
        self.dongle.powered = True
        self.assertEqual(True, self.dongle.powered)

    def test_adapter_discoverable(self):
        """
        Test the adapter ``discoverable`` property.
        """
        self.assertEqual(self.dongle.discoverable, False)

    def test_adapter_discoverable_write(self):
        """
        Test that the adapter ``discoverable`` property can be set.
        """
        self.dongle.discoverable = True
        self.assertEqual(True, self.dongle.discoverable)
        self.dongle.discoverable = False
        self.assertEqual(False, self.dongle.discoverable)

    def test_adapter_pairable(self):
        """
        Test the adapter ``pairable`` property.
        """
        self.assertTrue(self.dongle.pairable)

    def test_adapter_pairable_write(self):
        """
        Test that the adapter ``pairable`` property can be set.
        """
        current_val = self.dongle.pairable
        self.dongle.pairable = not current_val
        self.assertEqual(not current_val, self.dongle.pairable)
        self.dongle.pairable = current_val

    def test_adapter_pairabletimeout(self):
        """
        Test the adapter ``pairabletimeout`` property.
        """
        self.assertIsInstance(self.dongle.pairabletimeout, int)

    def test_adapter_pairabletimeout_write(self):
        """
        Test that the adapter ``pairabletimeout`` property can be set.
        """
        current_setting = self.dongle.pairabletimeout
        new_setting = current_setting + 220
        self.dongle.pairabletimeout = new_setting
        self.assertEqual(new_setting, self.dongle.pairabletimeout)

    def test_adapter_discoverable_timeout(self):
        """
        Test the adapter ``discoverabletimeout`` property.
        """
        self.assertEqual(180, self.dongle.discoverabletimeout)

    def test_adapter_discoverabletimeout_write(self):
        """
        Test that the adapter ``discoverabletimeout`` property can be set.
        """
        current_val = self.dongle.discoverabletimeout
        new_val = current_val + 220
        self.dongle.discoverabletimeout = new_val
        self.assertEqual(new_val, self.dongle.discoverabletimeout)
        self.dongle.discoverabletimeout = current_val

    def test_adapter_discovering(self):
        """
        Test the adapter ``discovering`` property.
        """
        self.assertEqual(False, self.dongle.discovering)

    @unittest.skip('mock of discovery not implemented')
    def test_start_discovery(self):
        """
        Test the adapter ``nearby_discovering()`` method.
        """
        self.dongle.nearby_discovery()
        self.assertEqual(True, self.dongle.discovering)


if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout,
                                                     verbosity=2))
