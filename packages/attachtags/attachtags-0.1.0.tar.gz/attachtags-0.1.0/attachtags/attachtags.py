"""Main module."""
import os
import platform
import pickle
from .parserbuilder import COMMANDS, build_parser
from .tagmaps import TagMaps
from .argtomap import arg_to_map

if platform.system() == "Windows":
    ATTACHTAGS_PATH = os.environ.get('USERPROFILE') + '\\.attachtags'
elif platform.system() == "Linux":
    ATTACHTAGS_PATH = os.environ.get('HOME') + '\\.attachtags'

PICKLE_PATH = ATTACHTAGS_PATH + '\\contents.pickle'
FILE_PATH = os.getcwd()


def create_default_maps(tag_maps):
    pass


def dump_pickle(tag_maps: TagMaps):
    with open(PICKLE_PATH, "wb") as f:
        pickle.dump(tag_maps, file=f)


def create_default_dir():
    os.mkdir(ATTACHTAGS_PATH)
    tag_maps = TagMaps()
    create_default_maps(tag_maps)
    dump_pickle(tag_maps)
    return tag_maps


def load_pickle() -> TagMaps:
    with open(PICKLE_PATH, 'rb') as f:
        tag_maps = pickle.load(f)
    return tag_maps


def _main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        tag_maps = load_pickle()
        assert type(tag_maps) is TagMaps
    except FileNotFoundError or AssertionError:
        tag_maps = create_default_dir()

    if args.list:
        map_ = tag_maps.get_map()
        for tag in map_.keys():
            print(f'{tag}:\n - '+' - \n'.join(map_[tag]))
    else:
        assert args.key_ in COMMANDS
        arg_to_map(args, tag_maps)
        dump_pickle(tag_maps)

    # print(args.__dict__)
    # print(args.__dict__.keys())
    # print(tag_maps.get_map())


if __name__ == "__main__":
    _main()
