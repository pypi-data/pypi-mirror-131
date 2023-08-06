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

class CompilerNotFound(Exception):
    pass


class CompilationError(Exception):
    pass


class WrongSourceFound(Exception):
    pass


class LanguageNotSupported(Exception):
    pass


class AssignmentTestDifferentValues(Exception):
    pass
