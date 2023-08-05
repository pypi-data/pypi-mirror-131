import flood_napari
import pytest

# this is your plugin name declared in your napari.plugins entry point
MY_PLUGIN_NAME = "flood-napari"
# the name of your widget(s)
MY_WIDGET_NAMES = ["Qt_Designer_flood", "flood_magic_factory", "FunctionGui_flood"]


@pytest.mark.parametrize("widget_name", MY_WIDGET_NAMES)
def test_something_with_viewer(widget_name, make_napari_viewer, napari_plugin_manager):
    napari_plugin_manager.register(flood_napari, name=MY_PLUGIN_NAME)
    viewer = make_napari_viewer()
    num_dw = len(viewer.window._dock_widgets)
    viewer.window.add_plugin_dock_widget(
        plugin_name=MY_PLUGIN_NAME, widget_name=widget_name
    )
    assert len(viewer.window._dock_widgets) == num_dw + 1
