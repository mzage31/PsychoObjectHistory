import bpy
from . import pv_ui
from . import pv_types
from . import pv_operators
from . import pv_handlers
from . import pv_menus

bl_info = {
    "name": "PsychoVertex Object History",
    # "description": "",
    "author": "Mohammad Zamanian",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Properties > Object > Psycho History",
    # "wiki_url": "http://my.wiki.url",
    # "tracker_url": "http://my.bugtracker.url",
    # "support": "COMMUNITY",
    "category": "Object"
}


def register():
    pv_ui.register()
    pv_types.register()
    pv_operators.register()
    pv_handlers.register()
    pv_menus.register()


def unregister():
    pv_ui.unregister()
    pv_types.unregister()
    pv_operators.unregister()
    pv_handlers.unregister()
    pv_menus.unregister()


if __name__ == "__main__":
    register()
