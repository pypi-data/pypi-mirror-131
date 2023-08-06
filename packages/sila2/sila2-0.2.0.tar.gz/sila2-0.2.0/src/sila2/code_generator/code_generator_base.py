import os
import sys
from os.path import exists

from sila2.code_generator.template_environment import TemplateEnvironment


class CodeGeneratorBase:
    overwrite: bool
    template_env: TemplateEnvironment

    def __init__(self, overwrite: bool = False) -> None:
        self.overwrite = overwrite
        self.template_env = TemplateEnvironment()

    def generate_file(self, out_filename: str, content: str, *, allow_overwrite: bool = False) -> None:
        if exists(out_filename) and open(out_filename).read() != content and not (self.overwrite or allow_overwrite):
            raise FileExistsError(f"File '{out_filename}' already exists. Set --overwrite to overwrite existing files.")
        with open(out_filename, "w") as fp:
            fp.write(content)

        if out_filename.endswith((".py", ".pyi")):
            os.system(f"{sys.executable} -m isort --line-length 120 --quiet --profile black {out_filename}")
            os.system(f"{sys.executable} -m black --line-length 120 --quiet {out_filename}")

    def generate_directory(self, dir_: str, *, allow_overwrite: bool = False) -> None:
        if exists(dir_) and os.listdir(dir_) and not (self.overwrite or allow_overwrite):
            raise FileExistsError(f"Directory '{dir_}' already exists. Set --overwrite to overwrite existing files.")
        os.makedirs(dir_, exist_ok=True)
