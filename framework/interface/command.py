# (void)walker command line interface
# Copyright (C) 2012 David Holm <dholmster@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict

from ..utils.decorators import singleton
from ..utils.decorators import singleton_specification


class Command(object):
    def __init__(self):
        self._config = None
        self._terminal = None

    def init(self, config, terminal):
        self._config = config
        self._terminal = terminal


class PrefixCommand(Command):
    def invoke(self, *_):
        self._terminal.write('%(face-error)sAttempting to invoke an '
                             'incomplete command!\n')


class DataCommand(Command):
    def invoke(self, thread, argument, from_tty=False):
        raise NotImplementedError


class StackCommand(Command):
    def invoke(self, thread, argument, from_tty=False):
        raise NotImplementedError


class BreakpointCommand(Command):
    def invoke(self, inferior, argument, from_tty=False):
        raise NotImplementedError


class SupportCommand(Command):
    def invoke(self, argument, from_tty=False):
        raise NotImplementedError


@singleton_specification
class CommandFactory(object):
    def create_command(self, command_type):
        raise NotImplementedError


@singleton
class CommandManager(object):
    def __init__(self):
        self._commands = OrderedDict()
        self._instances = {}

    def init(self, config, terminal):
        for name, Cmd in self._commands.iteritems():
            self._instances[name] = CommandFactory().create_command(Cmd)
            self._instances[name].init(config, terminal)

    def commands(self):
        return self._commands.iteritems()

    def command(self, name):
        assert name in self._commands
        return self._commands[name]

    def add_command(self, command):
        self._commands[command.name()] = command


def register_command(cls):
    CommandManager().add_command(cls)
    return cls
