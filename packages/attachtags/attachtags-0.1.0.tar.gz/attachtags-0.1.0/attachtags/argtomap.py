import argparse
import os
from .tagmaps import TagMaps


def _create(arg, tag_maps: TagMaps):
    for tag in arg.new_tag:
        tag_maps.create(tag)


def _delete(arg, tag_maps: TagMaps):
    for tag in arg.goal_tag:
        tag_maps.delete(tag)


def _rename(arg, tag_maps: TagMaps):
    for tag in arg.old_name:
        tag_maps.rename(tag, arg.new_name[0])


def _show(arg, tag_maps: TagMaps):
    for f in arg.file:
        f = os.path.abspath(f)
        if not os.path.isfile(f):
            print(f"File {f} not found")
            break
    else:
        if arg.some:
            for f in arg.file:
                abs_f = os.path.abspath(f)
                tag_set = tag_maps.show(abs_f)
                print(f"{abs_f}:\n - {' '.join(tag_set)}")
        # elif arg.use_pickle:
        #     pass
        else:
            if len(arg.file) == 1:
                tag_set = tag_maps.show(os.path.abspath(arg.file[0]))
                print(f"{' '.join(tag_set)}")
            else:
                print("Must one file")


def _search_in_dir(dir, arg, tag_maps: TagMaps):
    goal_list = set()
    for f in os.listdir(dir):
        rel_f = os.path.join(dir, f)
        if os.path.isfile(rel_f):
            if tag_maps.search(arg.tags, rel_f):
                goal_list.add(rel_f)
        elif os.path.isdir(rel_f) and arg.include_dir:
            goal_list.update(
                _search_in_dir(rel_f, arg, tag_maps)
                )
        else:
            pass
    return goal_list


def _search(arg, tag_maps: TagMaps):
    abs_path = os.path.abspath(arg.goal_path)
    if not os.path.isdir(abs_path):
        print(f"Dir {arg.goal_path} not found")
    else:
        goal_list = _search_in_dir(abs_path, arg, tag_maps)
        if arg.abs:
            print('\n'.join(goal_list))
        else:
            print(' '.join(
                map(os.path.relpath, goal_list)
                ))


def _attach_in_dir(dir, arg, tag_maps: TagMaps):
    for f in os.listdir(dir):
        f = os.path.join(dir, f)
        if os.path.isfile(f):
            tag_maps.attach(arg.tag, f)
        elif os.path.isdir(f):
            _attach_in_dir(f, arg, tag_maps)
        else:
            pass


def _attach(arg, tag_maps: TagMaps):
    if arg.all_in_dirs:
        for f in arg.files:
            f = os.path.abspath(f)
            if not os.path.isdir(f):
                print(f"Dir {f} not found, skipping")
            else:
                _attach_in_dir(f, arg, tag_maps)
    # elif arg.use_pickle:
    #     pass
    else:
        for f in arg.files:
            f = os.path.abspath(f)
            if not os.path.isfile(f):
                print(f"File {f} not found, skipping")
            else:
                tag_maps.attach(arg.tag, f)


def _remove_in_dir(dir, arg, tag_maps: TagMaps):
    for f in os.listdir(dir):
        f = os.path.join(dir, f)
        if os.path.isfile(f):
            tag_maps.remove(arg.tag, f)
        elif os.path.isdir(f):
            _remove_in_dir(f, arg, tag_maps)
        else:
            pass


def _remove(arg, tag_maps: TagMaps):
    if arg.all_in_dirs:
        for f in arg.files:
            f = os.path.abspath(f)
            if not os.path.isdir(f):
                print(f"Dir {f} not found, skipping")
            else:
                _remove_in_dir(f, arg, tag_maps)
    # elif arg.use_pickle:
    #     pass
    else:
        for f in arg.files:
            f = os.path.abspath(f)
            if not os.path.isfile(f):
                print(f"File {f} not found, skipping")
            else:
                tag_maps.remove(arg.tag, f)


# def _export(arg, tag_maps: TagMaps):
#     pass


def arg_to_map(arg: argparse.ArgumentParser, tag_maps: TagMaps):
    exec("_"+arg.key_+"(arg, tag_maps)")
