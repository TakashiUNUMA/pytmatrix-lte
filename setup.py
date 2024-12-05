"""
Copyright (C) 2009-2017 Jussi Leinonen, Finnish Meteorological Institute, 
California Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""



from setuptools import setup, Extension
import numpy
import sys
import subprocess
import os
import warnings
import shutil
import sysconfig
import glob


cwd = os.getcwd()
# so_file = f'pytmatrix.cpython-{sys.version_info[0]}{sys.version_info[1]}-x86_64-linux-gnu.so'
# target_dir = cwd+f'/build/lib.linux-x86_64-cpython-{sys.version_info[0]}{sys.version_info[1]}/pytmatrix/fortran_tm/'

extension_suffix = sysconfig.get_config_var('EXT_SUFFIX')
# Build the pattern to search for the extension file
extension_pattern = os.path.join(os.path.expanduser('~/pytmatrix/'), f"*{extension_suffix}")
# Use glob to search for the compiled extension file
compiled_files = glob.glob(extension_pattern)
extension_file = compiled_files[0] if compiled_files else None

platform_info = sysconfig.get_platform()
python_version = f"cpython-{sys.version_info[0]}{sys.version_info[1]}"  # e.g., cpython-312
target_dir = os.path.join(cwd+'/build/', f'lib.{platform_info}-{python_version}/pytmatrix/fortran_tm/')

def build_fortran_extension():
    # Make sure the Fortran source files are compiled using f2py
    sources = [
        'pytmatrix/fortran_tm/pytmatrix.pyf',
        'pytmatrix/fortran_tm/ampld.lp.f',
        'pytmatrix/fortran_tm/lpd.f'
    ]
    
    # Compile Fortran code using f2py
    fortran_sources = [src for src in sources if src.endswith('.f')]
    fortran_sources.extend([src for src in sources if src.endswith('.pyf')])  # Include .pyf files as well

    # Use f2py to compile Fortran sources
    # for src in fortran_sources:
    cmd = ['f2py', '-c', '-m', 'fortran_tm.pytmatrix', '-I', cwd+'/pytmatrix/fortran_tm/'] + sources
    subprocess.check_call(cmd)


def move_fortran_extension_files(so_file, target_dir):
    # After compilation, move the extension file (.so) to the appropriate directory
    # for some reason we need to do this manually because the .so file is not moved to the correct directory
    
    if not os.path.isfile(so_file):
        warnings.warn("Could not find the extension file {so_file}, moving on.")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Move the .so file to the target directory  
    shutil.copy(so_file, os.path.join(target_dir, os.path.basename(so_file)))
    print(f"Moved {so_file} to {target_dir}")



def configuration(parent_package='', so_file='', target_dir='', top_path=None):
    # Package metadata
    long_description =   "A Python code for computing the scattering properties of homogeneous nonspherical scatterers with the T-Matrix method. Requires NumPy and SciPy. "


    # Fortran extension setup (no distutils or custom build_ext)
    kw = {}
    if sys.platform == 'darwin':
        kw['extra_link_args'] = ['-undefined dynamic_lookup', '-bundle']

    # You can define a basic Extension, but the Fortran compilation is handled separately
    fortran_extension = Extension(
        'fortran_tm.pytmatrix',
        sources = [
    ],
        **kw
    )

    # Call the Fortran compilation before setup
    build_fortran_extension()

    # Move the compiled Fortran extension files to the correct directory
    move_fortran_extension_files(so_file, target_dir)

    # Package setup
    setup(
        name='pytmatrix',
        version='0.3.3',
        author= "Jussi Leinonen",
        author_email="jsleinonen@gmail.com",
        description="T-matrix scattering computations",
        license='MIT',
        url='https://github.com/jleinonen/pytmatrix',
        download_url='https://github.com/jleinonen/pytmatrix/releases/download/0.3.3/pytmatrix-0.3.3.zip',
        long_description=long_description,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Fortran",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Physics",
        ],
        ext_modules=[fortran_extension],
        packages = ['pytmatrix','pytmatrix.test','pytmatrix.quadrature',
            'pytmatrix.fortran_tm'],
        package_data = {
            'pytmatrix': ['ice_refr.dat'],
            'pytmatrix.fortran_tm': ['ampld.par.f']
        },
        install_requires=['numpy', 'scipy'],  # You can add any other dependencies here
    )

if __name__ == '__main__':
    print(target_dir)
    configuration(so_file=extension_file, target_dir=target_dir)