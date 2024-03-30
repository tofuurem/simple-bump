import os
import sys
from pathlib import Path

from simple_bump.core.files_operation import FilesOperation
from simple_bump.core.git_operation import GitOperations


class Core:
    def __init__(self) -> None:
        rel_path = Path(os.path.dirname(os.path.abspath(sys.argv[1])))
        self.go = GitOperations(rel_path)
        self.fo = FilesOperation(rel_path)



