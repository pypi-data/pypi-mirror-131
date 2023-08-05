# -*- coding: utf-8 -*-
# Copyright 2021, SERTIT-ICube - France, https://sertit.unistra.fr/
# This file is part of eoreader project
#     https://github.com/sertit/eoreader
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
COSMO-SkyMed products.
More info `here <https://earth.esa.int/documents/10174/465595/COSMO-SkyMed-Mission-Products-Description>`_.
"""
import logging
import warnings
from enum import unique

import rasterio
from sertit.misc import ListEnum

from eoreader.exceptions import InvalidProductError
from eoreader.products.sar.cosmo_product import CosmoProduct
from eoreader.utils import EOREADER_NAME

LOGGER = logging.getLogger(EOREADER_NAME)

# Disable georef warnings here as the SAR products are not georeferenced
warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)


@unique
class CskSensorMode(ListEnum):
    """
    COSMO-SkyMed sensor mode.
    Take a look `here <https://earth.esa.int/documents/10174/465595/COSMO-SkyMed-Mission-Products-Description>`_.
    """

    HI = "HIMAGE"
    """Himage"""

    PP = "PINGPONG"
    """PingPong"""

    WR = "WIDEREGION"
    """Wide Region"""

    HR = "HUGEREGION"
    """Huge Region"""

    S2 = "ENHANCED SPOTLIGHT"
    """Enhanced Spotlight"""


class CskProduct(CosmoProduct):
    """
    Class for COSMO-SkyMed Products

    .. code-block:: python

        >>> from eoreader.reader import Reader
        >>> # CSK products could have any folder but needs to have a .h5 file correctly formatted
        >>> # ie. "CSKS1_SCS_B_HI_15_HH_RA_SF_20201028224625_20201028224632.h5"
        >>> path = r"1011117-766193"
        >>> prod = Reader().open(path)
    """

    def _set_resolution(self) -> float:
        """
        Set product default resolution (in meters)
        """
        # Read metadata for default resolution
        try:
            root, _ = self.read_mtd()
            def_res = float(root.findtext(".//GroundRangeGeometricResolution"))
        except (InvalidProductError, TypeError):
            raise InvalidProductError(
                "GroundRangeGeometricResolution or rowSpacing not found in metadata!"
            )

        return def_res

    def _set_sensor_mode(self) -> None:
        """
        Get products type from S2 products name (could check the metadata too)
        """
        # Get MTD XML file
        root, _ = self.read_mtd()

        # Open identifier
        try:
            acq_mode = root.findtext(".//AcquisitionMode")
        except TypeError:
            raise InvalidProductError("AcquisitionMode not found in metadata!")

        # Get sensor mode
        self.sensor_mode = CskSensorMode.from_value(acq_mode)

        if not self.sensor_mode:
            raise InvalidProductError(
                f"Invalid {self.platform.value} name: {self.name}"
            )
