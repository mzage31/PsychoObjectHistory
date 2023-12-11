import bpy
import re


def flatten(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


def strip_trailing_number(s):
    m = re.search(r'\.(\d{3})$', s)
    return s[0:-4] if m else s


def unique_name(collection, base_name):
    base_name = strip_trailing_number(base_name)
    count = 1
    name = base_name

    while collection.get(name):
        name = f"{base_name}.{count:03d}"
        count += 1
    return name


def replace_objects(old: bpy.types.Object, new: bpy.types.Object):
    if old == new:
        return
    old.select_set(False)

    if old.users_collection:
        old.users_collection[0].objects.link(new)
        old.users_collection[0].objects.unlink(old)
    else:
        print("ERROR: objects are not in a collection")
        return

    new.location = old.location
    new.rotation_euler = old.rotation_euler
    new.scale = old.scale

    new.select_set(True)
    bpy.context.view_layer.objects.active = new
