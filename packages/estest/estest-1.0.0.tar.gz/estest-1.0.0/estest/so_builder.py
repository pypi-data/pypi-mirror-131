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

import compilers
import language_codes
import exceptions
import os
from typing import List


class SharedObjectBuilder:
    def __init__(self, compiler: compilers.Compiler, sources: List[str], output_shared_object: str):
        if not compiler.exists():
            raise exceptions.CompilerNotFound(
                "compiler `{}` was not found in your OS".format(compiler.name))
        self.compiler = compiler
        self.sources = sources
        self.output_shared_object = output_shared_object

    def detect_language(self) -> int:
        current_language_code: int = 0
        global_language_code: int = 0
        for source in self.sources:
            if source.endswith(".c"):
                current_language_code = language_codes.LANGUAGE_C
            elif source.endswith(".cpp"):
                current_language_code = language_codes.LANGUAGE_CPP
            else:
                raise exceptions.WrongSourceFound(
                    "ESTEST cannot handle language of {}".format(source))
            global_language_code = max(
                current_language_code, global_language_code)
        return global_language_code

    def build_sources(self) -> int:
        return os.system(self.compiler.compile_command_format.format(
            " ".join(self.sources),
            self.output_shared_object))

    def build(self) -> int:
        language = self.detect_language()
        if self.compiler.language_code < language:
            raise exceptions.LanguageNotSupported("The compiler is not suitable for compilation of {} language.".format(
                language_codes.language_code_to_string(language)))
        compilation_return_code: int = self.build_sources()
        if compilation_return_code != 0:
            raise exceptions.CompilationError(
                "Compilation failed with code: {}".format(compilation_return_code))

    def __str__(self) -> str:
        return "ESTEST.SharedObjectBuilder(compiler=`{}`, sources={})".format(self.compiler.name, self.sources)
