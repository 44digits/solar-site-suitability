"""Tests for the Solar Site Selection ArcGIS toolbox."""

import importlib.util
from importlib.machinery import SourceFileLoader
import sys
import types
from pathlib import Path

import pytest


PYT_FILE = Path(__file__).parents[1] / "SolarSiteSelection.pyt"


class FakeParameter:
    """Minimal ArcPy parameter replacement for toolbox metadata tests."""

    def __init__(self, **properties: object) -> None:
        self.__dict__.update(properties)
        self.value = None
        self.filter = types.SimpleNamespace(type=None, list=None)
        self.error_message = None

    def setErrorMessage(self, message: str) -> None:
        self.error_message = message


@pytest.fixture
def toolbox_module(monkeypatch: pytest.MonkeyPatch) -> types.ModuleType:
    """Load the Python toolbox with a minimal ArcPy replacement."""
    arcpy = types.ModuleType("arcpy")
    arcpy.Parameter = FakeParameter  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "arcpy", arcpy)

    loader = SourceFileLoader("SolarSiteSelection", str(PYT_FILE))
    spec = importlib.util.spec_from_file_location(
        "SolarSiteSelection", PYT_FILE, loader=loader
    )
    assert spec is not None and spec.loader is not None

    toolbox_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(toolbox_module)
    return toolbox_module


def test_toolbox_name(toolbox_module: types.ModuleType) -> None:
    """The toolbox exposes the expected display name."""
    assert toolbox_module.Toolbox().label == "Solar Site Suitability Analysis"


def test_tool_parameters(toolbox_module: types.ModuleType) -> None:
    """The toolbox exposes the expected layers, download flags, and weights."""
    parameters = toolbox_module.Tool().getParameterInfo()

    assert [parameter.displayName for parameter in parameters[:4]] == [
        "Digital Elevation Model",
        "Solar Irradiance (GHI/DNI)",
        "Electrical Transmission Infrastructure",
        "Environmental Exclusions",
    ]
    assert [parameter.datatype for parameter in parameters[4:8]] == [
        "GPBoolean",
    ] * 4
    assert [parameter.value for parameter in parameters[4:8]] == [False] * 4
    assert [parameter.displayName for parameter in parameters[8:]] == [
        "Weight of Digital Elevation Model",
        "Weight of Solar Irradiance",
        "Weight of Electrical Transmission Infrastructure",
        "Weight of Environmental Exclusions",
    ]
    assert [parameter.datatype for parameter in parameters[8:]] == ["GPLong"] * 4
    assert [parameter.filter.list for parameter in parameters[8:]] == [[0, 100]] * 4


def test_tool_validates_weights_sum_to_100(
    toolbox_module: types.ModuleType,
) -> None:
    """The tool rejects weight values that do not total 100."""
    tool = toolbox_module.Tool()
    parameters = tool.getParameterInfo()
    for parameter, value in zip(parameters[8:], [25, 25, 25, 24]):
        parameter.value = value

    tool.updateMessages(parameters)

    assert parameters[8].error_message == "Weights must sum to 100."

    for parameter in parameters[8:]:
        parameter.value = 25
        parameter.error_message = None

    tool.updateMessages(parameters)

    assert parameters[8].error_message is None
