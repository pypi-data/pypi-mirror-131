from setuptools import find_packages, setup
from setuptools import Extension
from distutils.command.build import build as build_orig
# import numpy as np

__version__ = "0.0.11"

# import Cython.Compiler.Options
# Cython.Compiler.Options.annotate = True

with open("README.md", 'r') as f:
    long_description = f.read()

# import Cython.Compiler.Options
# Cython.Compiler.Options.annotate = True

exts = [Extension(name='fastash.ashfunc',
                  sources=["fastash/ashfunc.pyx"],
                  include_dirs=["fastash"])]

class build(build_orig):

    def finalize_options(self):
        super().finalize_options()
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        for extension in self.distribution.ext_modules:
            extension.include_dirs.append(numpy.get_include())
        from Cython.Build import cythonize
        self.distribution.ext_modules = cythonize(self.distribution.ext_modules,
                                                  language_level=3)

setup(
     name="fastash",
     version=__version__,
     author="François-Rémi Mazy",
     author_email="francois-remi.mazy@inria.fr",
     license="BSD 3-Clause License",
     description="Fast Averaged Shifted Histogram module.",
     long_description=long_description,
     long_description_content_type='text/markdown',
     packages=find_packages(),
     url="https://gitlab.inria.fr/fmazy/fastash",
     ext_modules=exts,
     zip_safe=False,
     setup_requires=["cython", "numpy"],
     install_requires=[
        'numpy>=1.20.3',
    ],
     cmdclass={"build": build},
)    
