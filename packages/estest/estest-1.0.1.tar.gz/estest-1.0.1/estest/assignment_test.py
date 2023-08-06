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

from estest import exceptions
from typing import Generic, TypeVar, List
from threading import Thread

T = TypeVar('T')


class AssignmentTestUnit(Generic[T]):
    def __init__(self, left: List[T], right: List[T]):
        self.left = left
        self.right = right

    def start(self):
        Thread(target=self.run).start()

    def run(self):
        if len(self.left) != len(self.right):
            raise exceptions.AssignmentTestDifferentValues(
                "Length of self.left: {} != length of self.right: {}".format(
                    self.left,
                    self.right))
        for index in range(len(self.left)):
            if self.left[index] != self.right[index]:
                raise exceptions.AssignmentTestDifferentValues(
                    "self.left[{1}] != self.right[{1}]: {2} != {3}".format(
                        index,
                        self.left[index],
                        self.right[index]
                    )
                )
        print("tests passed")
