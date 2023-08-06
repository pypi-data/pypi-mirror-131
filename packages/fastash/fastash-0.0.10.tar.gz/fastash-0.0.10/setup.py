from setuptools import find_packages, setup
from Cython.Build import cythonize
import numpy as np

# import Cython.Compiler.Options
# Cython.Compiler.Options.annotate = True

with open("README.md", 'r') as f:
    long_description = f.read()

# import Cython.Compiler.Options
# Cython.Compiler.Options.annotate = True


setup(
     name="fastash",
     version="0.0.10",
     packages=find_packages(),
     author="François-Rémi Mazy",
     description="Fast Averaged Shifted Histogram module.",
     long_description=long_description,
     long_description_content_type='text/markdown',
     url="https://gitlab.inria.fr/fmazy/fastash",
     ext_modules=cythonize(["fastash/ashfunc.pyx"]),
     include_dirs=np.get_include(),
     install_requires=[
        'numpy>=1.20.3',
    ]
)    
