"""这个模块定义了Tagmaps类型
"""
from functools import wraps


def exist_or_not(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs) -> bool:
        if args[0] in list(self.get_map().keys()):
            function(self, *args, **kwargs)
            return True
        else:
            print(f"""Fail {function.__name__}
 - not the tag: {args[0]}""", end="")
            if len(args) > 1:
                print(f""" for {args[1]}""")
            else:
                print('\n')
            return False
    return wrapper


class TagMaps:
    def __init__(self):
        self.__map = dict()
        self.tagnames = set()

    def get_map(self) -> dict:
        return self.__map

    def create(self, new_name):
        if new_name not in list(self.__map.keys()):
            self.__map[new_name] = set()
            return True
        else:
            print(f"tag {new_name} has already existed")
            return False

    @exist_or_not
    def delete(self, goal):
        del self.__map[goal]

    @exist_or_not
    def rename(self, old_name, new_name):
        if not self.create(new_name):
            print("two tags were merged")
        self.__map[new_name].update(self.__map[old_name])
        self.delete(old_name)

    def show(self, goal: str) -> set:
        tag_set = set()
        for tag in self.__map.keys():
            if goal in self.__map[tag]:
                tag_set.add(tag)
        return tag_set

    def search(self, tags, file):
        for tag in tags:
            if file in self.__map[tag]:
                return True
            return False

    @exist_or_not
    def attach(self, tag, file):
        if file not in self.__map[tag]:
            self.__map[tag].add(file)
        else:
            print(f"{file} was existed, skipping")

    @exist_or_not
    def remove(self, tag, file):
        if file in self.__map[tag]:
            self.__map[tag].remove(file)
        else:
            print(f"{file} is not with {tag}")


if __name__ == '__main__':
    tag = TagMaps()
    if tag.create('foo'):
        print(tag.rename('foo', 'bar'))
