# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2015-2017 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from testtools.matchers import Equals, Contains

from snapcraft.tests import fixture_setup
from . import CommandBaseTestCase


class ListPluginsCommandTestCase(CommandBaseTestCase):

    scenarios = [
        ('list-plugins', {'command_name': 'list-plugins'}),
        ('plugins alias', {'command_name': 'plugins'}),
    ]

    # plugin list when wrapper at MAX_CHARACTERS_WRAP
    default_plugin_output = (
            'ant        cmake  go      gulp    kernel  meson   '
            'plainbox-provider  python3  scons      \n'
            'autotools  copy   godeps  jdk     make    nil     '
            'python             qmake    tar-content\n'
            'catkin     dump   gradle  kbuild  maven   nodejs  '
            'python2            rust     waf        \n'
    )

    def test_list_plugins_non_tty(self):
        self.maxDiff = None
        fake_terminal = fixture_setup.FakeTerminal(isatty=False)
        self.useFixture(fake_terminal)

        result = self.run_command([self.command_name])

        self.assertThat(result.exit_code, Equals(0))
        self.assertThat(result.output, Contains(self.default_plugin_output))

    def test_list_plugins_large_terminal(self):
        self.maxDiff = None
        fake_terminal = fixture_setup.FakeTerminal(columns=999)
        self.useFixture(fake_terminal)

        result = self.run_command([self.command_name])

        self.assertThat(result.exit_code, Equals(0))
        self.assertThat(result.output, Contains(self.default_plugin_output))

    def test_list_plugins_small_terminal(self):
        self.maxDiff = None
        fake_terminal = fixture_setup.FakeTerminal(columns=60)
        self.useFixture(fake_terminal)

        expected_output = (
            'ant        go      kernel  plainbox-provider  scons      \n'
            'autotools  godeps  make    python             tar-content\n'
            'catkin     gradle  maven   python2            waf        \n'
            'cmake      gulp    meson   python3          \n'
            'copy       jdk     nil     qmake            \n'
            'dump       kbuild  nodejs  rust             \n'
        )

        result = self.run_command([self.command_name])

        self.assertThat(result.exit_code, Equals(0))
        self.assertThat(result.output, Contains(expected_output))
