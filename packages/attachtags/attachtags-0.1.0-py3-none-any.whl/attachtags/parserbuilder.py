"""创建命令行解析器
"""
import argparse as ap
from .__init__ import __version__


COMMANDS = (
    "create",
    "delete",
    "rename",
    "show",
    "search",
    "attach",
    # "export",
    "remove"
)


def add_key(goal: ap.ArgumentParser):
    goal.add_argument("key_",
                      action="store_const",
                      const=goal.prog.split(' ')[-1],
                      help="id of the command, ignore it"
                      )


def add_create_parse(subparsers: ap._SubParsersAction):
    create = subparsers.add_parser(
        "create",
        help="create one new tag")
    create.add_argument("new_tag",
                        type=str,
                        nargs="+",
                        help="new tag")
    add_key(create)


def add_delete_parse(subparsers):
    delete = subparsers.add_parser(
        "delete",
        help="delete one tag")
    delete.add_argument("goal_tag",
                        type=str,
                        nargs="+",
                        help="goal tag")
    add_key(delete)


def add_rename_parse(subparsers):
    rename = subparsers.add_parser(
        "rename",
        help="rename some tags with a new name")
    rename.add_argument("old_name",
                        type=str,
                        nargs="+",
                        help="old name")
    rename.add_argument("new_name",
                        type=str,
                        nargs=1,
                        help="new name")
    add_key(rename)


def add_show_parse(subparsers):
    show = subparsers.add_parser(
        "show",
        help="show tags from some file")
    show.add_argument("file",
                      type=str,
                      nargs="+",
                      help="one file you want to show")
    man_show = show.add_mutually_exclusive_group()
    man_show.add_argument("-s", "--some",
                          action="store_true",
                          default=False,
                          help="show some files")
    # man_show.add_argument("--use-pickle", action="store_true",
    #                       default=False, help="use pickle")
    add_key(show)


def add_search_parse(subparsers):
    search = subparsers.add_parser(
        "search",
        help="search files with this tags in this path")
    search.add_argument("goal_path",
                        type=str,
                        nargs='?',
                        help="path you want to search in, must one")
    search.add_argument("tags",
                        type=str,
                        nargs="+",
                        help="tag you want to search")
    search.add_argument("--include-dir",
                        action="store_true",
                        default=False,
                        help="iterate over folders")
    search.add_argument("-a", "--abs",
                        action="store_true",
                        default=False,
                        help="the output path will be absolute path")
    # search.add_argument("--export-pickle", action="store_true",
    #                     default=False,
    #                     help="export the output as .pickle")
    add_key(search)


def add_attach_parse(subparsers):
    attach = subparsers.add_parser(
        "attach",
        help="attach a tag to some files")
    attach.add_argument("files",
                        type=str,
                        nargs="+",
                        help="file you want to attach to")
    attach.add_argument("tag",
                        type=str,
                        # nargs='?',
                        help="tag you want to attach")

    man_attach = attach.add_mutually_exclusive_group()
    man_attach.add_argument("--all-in-dirs",
                            action="store_true",
                            default=False,
                            help="attach tag to files all in path you \
                                enter,replacing files with some paths")
    # man_attach.add_argument("--use-pickle",
    #                         action="store_true",
    #                         default=False,
    #                         help="replace file with .pickle you enter")
    add_key(attach)


def add_remove_parse(subparsers):
    remove = subparsers.add_parser(
        "remove",
        help="remove a tag from some files")
    remove.add_argument("files",
                        type=str,
                        nargs="+",
                        help="file you want to remove on")
    remove.add_argument("tag",
                        type=str,
                        # nargs='?',
                        help="tag you want to remove")

    man_remove = remove.add_mutually_exclusive_group()
    man_remove.add_argument("--all-in-dirs",
                            action="store_true",
                            default=False,
                            help="remove tag from files all in paths you \
                               enter, replacing file with some paths")
    # man_remove.add_argument("--use-pickle",
    #                         action="store_true",
    #                         default=False,
    #                         help="replace file with .pickle you enter")
    add_key(remove)


# def add_export_parse(subparsers):
#     export = subparsers.add_parser("export", help="export you tags")
#     export.add_argument("form",
#                         type=str,
#                         choices=["lnk", "pickle"],
#                         help="format you want to export with")
#     export.add_argument("tag",
#                         type=str,
#                         nargs="+",
#                         help="tagname you want to export")
#     export.add_argument("-s", "--some",
#                         action="store_true",
#                         default=False,
#                         help="export more tags")
#     # 导出同时符合多个tag的文件
#     add_key(export)


def build_parser():
    parser = ap.ArgumentParser()
    parser.add_argument("-v", "--version",
                        action="version",
                        version="%(prog)s {}".format(__version__))
    parser.add_argument("-l", "--list",
                        action="store_true",
                        default=False,
                        help="list all tags")
    subparsers = parser.add_subparsers()

    add_create_parse(subparsers)
    add_delete_parse(subparsers)
    add_rename_parse(subparsers)

    add_show_parse(subparsers)

    add_search_parse(subparsers)
    add_attach_parse(subparsers)
    add_remove_parse(subparsers)

    # add_export_parse(subparsers)

    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    print(args)
