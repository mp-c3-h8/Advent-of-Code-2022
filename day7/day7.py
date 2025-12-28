import os.path
from dataclasses import dataclass, field
from typing import ClassVar

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
data = open(input_path).read().splitlines()


@dataclass
class File:
    name: str
    size: int


@dataclass
class Folder:
    folder_sizes: ClassVar[list[int]] = []
    name: str
    parent: Folder | None
    size: int = 0
    subfolders: dict[str, Folder] = field(default_factory=dict)
    files: list[File] = field(default_factory=list)

    def add_subfolder(self, name: str) -> None:
        self.subfolders[name] = Folder(name, self)

    def add_file(self, name: str, size: int) -> None:
        self.files.append(File(name, size))

    def print_tree(self, depth: int = 0) -> None:
        print("  "*depth, f"- {self.name} (dir - {self.size})")
        for folder in self.subfolders.values():
            folder.print_tree(depth+1)
        for f in self.files:
            print("  "*(depth+1), f"+ {f.name} ({f.size})")

    def calc_size(self) -> int:
        size = 0
        if self.files:
            size += sum(f.size for f in self.files)
        if self.subfolders:
            size += sum(f.calc_size() for f in self.subfolders.values())
        self.size = size
        Folder.folder_sizes.append(size)
        return size


root = Folder("/", None)

# its a tree with files as leafs
curr = root
for line in data:
    if line.startswith("$ ls"):
        continue
    elif line.startswith("$ cd"):
        folder = line[5:]
        if folder == "/":
            curr = root
        elif folder == "..":
            if curr.parent is not None:
                curr = curr.parent
        else:
            curr = curr.subfolders[folder]
    elif line.startswith("dir"):
        folder = line[4:]
        curr.add_subfolder(folder)
    else:  # file in current folder
        size_str, name = line.split(" ", 1)
        curr.add_file(name, int(size_str))

root_size = root.calc_size()
# root.print_tree()
print("Part 1:", sum(s for s in Folder.folder_sizes if s <= 100_000))
print("Part 2:", min(s for s in Folder.folder_sizes if 70_000_000 - root_size + s >= 30_000_000))
