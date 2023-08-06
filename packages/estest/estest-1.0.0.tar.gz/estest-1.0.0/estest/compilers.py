# This file is part of the Hike distribution (https://github.com/hikelang or http://hikelang.github.io).
# Copyright (c) 2021 Salimgereyev Adi.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import language_codes
from distutils.spawn import find_executable


class Compiler:
    def __init__(self, name: str, compile_command_format: str, language_code: int):
        self.name = name
        self.compile_command_format = compile_command_format
        self.language_code = language_code

    def exists(self) -> bool:
        """ Checks if compiler is installed in OS.
        """
        return find_executable(self.name) is not None

    def __str__(self) -> str:
        return "ESTEST.Compiler(name=`{}`, compile_command_format=`{}`)".format(self.name,
                                                                                self.compile_command_format)


GCC = Compiler(
    "gcc", "gcc -fPIC -shared -o {2} {1}", language_codes.LANGUAGE_C)
GPP = Compiler(
    "g++", "g++ -fPIC -shared -o {2} {1}", language_codes.LANGUAGE_CPP)
CLANG = Compiler(
    "clang", "clang -shared -undefined dynamic_lookup -o {2} {1}", language_codes.LANGUAGE_CPP)
