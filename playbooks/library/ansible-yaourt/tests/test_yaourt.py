#!/usr/bin/env python2
import os
import sys
import unittest
from mock import MagicMock, call

#src_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
#sys.path.insert(0, os.path.abspath(src_path))
from yaourt import Yaourt


class AnsibleModuleYaourtTests(unittest.TestCase):
    def setUp(self):
        self.mockModule = MagicMock()
        self.mockModule.run_command.return_value = [0, '', '']

    def tearDown(self):
        self.mockModule = None

    def testUpdateCache(self):
        self.runYaourt(['git'], 'present', update_cache=True)

        self.mockModule.run_command.assert_any_call(['yaourt', '-Su'])

    def testDontUpdateCacheByDefault(self):
        self.runYaourt(['git'], 'present')

        self.assertTrue(call.run_command(['yaourt', '-Su']) not in self.mockModule.method_calls)

    def testOnlyInstallsPackageIfItIsNotPresent(self):
        def run_command_stub(args):
            if (args == ['yaourt', '-Qi', 'git']):
                return (1, '', '')
            else:
                return (0, '', '')
        self.mockModule.run_command.side_effect = run_command_stub

        self.runYaourt(['git'], 'present')

        self.mockModule.run_command.assert_any_call(['yaourt', '-S', '--noconfirm', 'git'])

    def testOnlyRemovesPackageIfItIsInstalled(self):
        def run_command_stub(args):
            if (args == ['yaourt', '-Qi', 'git']):
                return (1, '', '')
            else:
                return (0, '', '')
        self.mockModule.run_command.side_effect = run_command_stub

        self.runYaourt(['git'], 'absent')

        self.assertTrue(call.run_command(['yaourt', '-R', '--noconfirm', 'git']) not in self.mockModule.method_calls)

    def runYaourt(self, pkgs, state, **kwargs):
        yaourt = self.createYaourtModule()
        yaourt.run(pkgs=pkgs, state=state, **kwargs)

    def createYaourtModule(self):
        return Yaourt(module=self.mockModule, path='yaourt')


if __name__ == '__main__':
    unittest.main()
