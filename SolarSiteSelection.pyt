# -*- coding: utf-8 -*-

"""ArcGIS toolbox for solar site suitability analysis.

This toolbox performs multi-criteria decision analysis (MCDA) to identify
optimal locations for utility-scale solar farms based on slope, solar
irradiance, proximity to grid infrastructure, and environmental restrictions.
"""

import arcpy
from typing import Any, List


class Toolbox:
    """Define the Solar Site Selection ArcGIS Python toolbox."""

    def __init__(self) -> None:
        """Initialize the toolbox metadata and registered tool classes."""
        self.label = "Solar Site Suitability Analysis"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool:
    """Provide the solar site suitability analysis geoprocessing tool."""

    def __init__(self) -> None:
        """Initialize the tool label and description shown in ArcGIS."""
        self.label = "Tool"
        self.description = ""

    def getParameterInfo(self) -> List[Any]:
        """Return the parameters accepted by the suitability analysis tool."""
        layer_parameters = [
            arcpy.Parameter(
                displayName="Digital Elevation Model",
                name="digital_elevation_model",
                datatype="GPRasterLayer",
                parameterType="Optional",
                direction="Input",
            ),
            arcpy.Parameter(
                displayName="Solar Irradiance (GHI/DNI)",
                name="solar_irradiance",
                datatype="GPRasterLayer",
                parameterType="Optional",
                direction="Input",
            ),
            arcpy.Parameter(
                displayName="Electrical Transmission Infrastructure",
                name="electrical_transmission_infrastructure",
                datatype="GPFeatureLayer",
                parameterType="Optional",
                direction="Input",
            ),
            arcpy.Parameter(
                displayName="Environmental Exclusions",
                name="environmental_exclusions",
                datatype="GPFeatureLayer",
                parameterType="Optional",
                direction="Input",
            ),
        ]

        download_parameters = [
            arcpy.Parameter(
                displayName=f"Download {display_name}",
                name=f"download_{name}",
                datatype="GPBoolean",
                parameterType="Required",
                direction="Input",
            )
            for name, display_name in (
                ("digital_elevation_model", "Digital Elevation Model"),
                ("solar_irradiance", "Solar Irradiance"),
                (
                    "electrical_transmission_infrastructure",
                    "Electrical Transmission Infrastructure",
                ),
                ("environmental_exclusions", "Environmental Exclusions"),
            )
        ]
        for parameter in download_parameters:
            parameter.value = False

        weight_parameters = []
        for name, display_name in (
            ("digital_elevation_model", "Digital Elevation Model"),
            ("solar_irradiance", "Solar Irradiance"),
            (
                "electrical_transmission_infrastructure",
                "Electrical Transmission Infrastructure",
            ),
            ("environmental_exclusions", "Environmental Exclusions"),
        ):
            parameter = arcpy.Parameter(
                displayName=f"Weight of {display_name}",
                name=f"weight_{name}",
                datatype="GPLong",
                parameterType="Required",
                direction="Input",
            )
            parameter.filter.type = "Range"
            parameter.filter.list = [0, 100]
            weight_parameters.append(parameter)

        return layer_parameters + download_parameters + weight_parameters

    def isLicensed(self) -> bool:
        """Return whether the current ArcGIS license permits execution."""
        return True

    def updateParameters(self, parameters: List[Any]) -> None:
        """Update parameter values and properties before ArcGIS validation.

        Args:
            parameters: The tool parameters managed by ArcGIS.
        """
        return

    def updateMessages(self, parameters: List[Any]) -> None:
        """Update validation messages after ArcGIS checks the parameters.

        Args:
            parameters: The tool parameters and validation messages managed by
                ArcGIS.
        """
        weights = [parameter.value for parameter in parameters[8:12]]
        if any(weight is None for weight in weights):
            return

        if sum(weights) != 100:
            parameters[8].setErrorMessage("Weights must sum to 100.")

    def execute(self, parameters: List[Any], messages: Any) -> None:
        """Run the solar site suitability analysis.

        Args:
            parameters: The validated inputs supplied to the tool.
            messages: The ArcGIS geoprocessing message interface.
        """
        return

    def postExecute(self, parameters: List[Any]) -> None:
        """Perform post-processing after outputs are added to the display.

        Args:
            parameters: The tool parameters supplied by ArcGIS.
        """
        return
