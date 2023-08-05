# hifis-surveyval
# Framework to help developing analysis scripts for the HIFIS Software survey.
#
# SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
This module provides a framework for plotters.

.. currentmodule:: hifis_surveyval.plotting.plotter
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from abc import ABC

from hifis_surveyval.core.settings import Settings


class Plotter(ABC):
    """Base class to derive plotters from."""

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """
        Initialize a plotter.

        Args:
            settings: (Settings):
                A Settings container to store the setup configuration
                in. It will be populated with the related settings during the
                initialization of the HIFISSurveyval object.
        """
        self.settings = settings
