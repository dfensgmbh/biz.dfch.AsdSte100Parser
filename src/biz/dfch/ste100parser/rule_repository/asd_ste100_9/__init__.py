# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""STE100 rule repository."""

from .r1_1_use_word_in_vocabulary import UseWordsInTheVocabulary
from .r3_6_use_active_voice import UseActiveVoice
from .r5_3_use_imperative_form import UseImperativeForm
from .r8_1_do_not_use_semicolon import DoNotUseSemicolon
from .rule_id import RuleId
from .ste100_rules import Ste100Rules

__all__ = [
    "UseWordsInTheVocabulary",
    "UseActiveVoice",
    "UseImperativeForm",
    "DoNotUseSemicolon",

    "RuleId",
    "Ste100Rules",
]
