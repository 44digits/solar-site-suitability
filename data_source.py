"""Base class for geospatial data sources used by the solar pipeline."""

from __future__ import annotations

from typing import Optional, Tuple, Union

import arcpy


DataValue = Union[arcpy.Raster, arcpy.FeatureSet, str]


class DataSource:
    """Common lifecycle operations for raster and vector data sources."""

    def __init__(
        self,
        name: str,
        xmin: float,
        ymin: float,
        xmax: float,
        ymax: float,
    ) -> None:
        """Initialize a data source and its study-area bounding box."""
        self.name = name
        self.bounding_box: Tuple[float, float, float, float] = (
            xmin,
            ymin,
            xmax,
            ymax,
        )
        self.data: Optional[DataValue] = None

    def fetch(self) -> bool:
        """Fetch the source data.

        Concrete data-source classes should override this method with their
        dataset-specific acquisition logic.
        """
        return False

    def delete(self) -> None:
        """Delete the fetched dataset and clear the in-memory reference."""
        if self.data is not None:
            arcpy.management.Delete(self.data)
            self.data = None

    def clip(self) -> None:
        """Clip the fetched raster or vector dataset to the bounding box."""
        if self.data is None:
            return

        xmin, ymin, xmax, ymax = self.bounding_box
        output_name = arcpy.CreateUniqueName(
            f"{self.name}_clipped",
            arcpy.env.scratchGDB,
        )
        description = arcpy.Describe(self.data)

        if description.dataType in {"RasterDataset", "RasterLayer"}:
            self.data = arcpy.management.Clip(
                self.data,
                f"{xmin} {ymin} {xmax} {ymax}",
                output_name,
            )[0]
            return

        spatial_reference = description.spatialReference
        clip_polygon = arcpy.Polygon(
            arcpy.Array(
                [
                    arcpy.Point(xmin, ymin),
                    arcpy.Point(xmin, ymax),
                    arcpy.Point(xmax, ymax),
                    arcpy.Point(xmax, ymin),
                    arcpy.Point(xmin, ymin),
                ]
            ),
            spatial_reference,
        )
        self.data = arcpy.analysis.Clip(
            self.data,
            clip_polygon,
            output_name,
        )[0]
