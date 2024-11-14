from distutils.core import setup
from Cython.Build import cythonize
from os import walk, path, remove, getcwd


needs_compiling = True

auto_remove = True


if auto_remove == True:
  for root, dirs, files in walk(getcwd()):
    for file in files:
      if file[-2:] == ".c":
        if path.exists(f"{file[:-2]}.cpython-38-x86_64-linux-gnu.so"):
          if not path.exists(f"{file[:-2]}.pyx"):
            remove(file)
            remove(f"{file[:-2]}.cpython-38-x86_64-linux-gnu.so")

if needs_compiling == True:
  setup(
    name="cython template",
    ext_modules=cythonize(
      ["*.pyx"], compiler_directives={"language_level": "3"}
    )
  )