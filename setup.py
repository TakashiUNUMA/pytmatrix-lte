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
import subprocess
import os
import numpy
import sys
from setuptools.command.build_ext import build_ext as _build_ext
import glob
import shutil

# Custom build extension class to invoke f2py manually
class PyTMatrixBuildExt(_build_ext):
    def run(self):
        # Call f2py to compile Fortran code into a Python extension
        self.build_fortran_extension()
        # Proceed with the usual build_ext behavior
        super().run()

    def build_fortran_extension(self):
        # Path to Fortran sources
        sources = [
            os.path.join('pytmatrix','fortran_tm','pytmatrix.pyf'),  # Interface file for f2py
            os.path.join('pytmatrix','fortran_tm','ampld.lp.f'),
            os.path.join('pytmatrix','fortran_tm','lpd.f')
        ]
        
        # The output module name should match the Python import path
        output_module = 'fortran_tm.pytmatrix'

        # Get the current working directory
        cwd = os.getcwd()
        include_dir = os.path.join(cwd, 'pytmatrix', 'fortran_tm')

        # Command to run f2py and compile the Fortran code into a shared object (.so)
        cmd = ['f2py', '-c', '-m', output_module, '-I', include_dir] + sources

        try:
            print("Running f2py command:", ' '.join(cmd))
            # Use subprocess.run to capture stdout and stderr
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Check for non-zero return code (indicating failure)
            if result.returncode != 0:
                print(f"f2py failed with error code {result.returncode}")
                print(f"Standard output:\n{result.stdout}")
                print(f"Standard error:\n{result.stderr}")
                raise subprocess.CalledProcessError(result.returncode, cmd)
            
            # After successful compilation, find the generated .so file
            compiled_so = glob.glob('*.so')
            if compiled_so:
                so_file = compiled_so[0]
                target_dir = os.path.join('pytmatrix','fortran_tm')
                
                # Ensure the target directory exists
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Move the .so file to the correct directory
                shutil.move(so_file, os.path.join(target_dir, so_file))
                print(f"Moved {so_file} to {target_dir}")

        except subprocess.CalledProcessError as e:
            print(f"f2py failed with error code {e.returncode}")
            raise


        # Run the f2py command to compile the extension
        print("Running f2py to compile Fortran sources:")
        subprocess.check_call(cmd)

        # The compiled shared object (.so file) will be placed in the current directory.

# Basic metadata about your package
setup(
    name='pytmatrix',
    version='0.3.3',
    author= "Jussi Leinonen",
    author_email="jsleinonen@gmail.com",
    description="T-matrix scattering computations",
    license='MIT',
    long_description='A Python code for computing the scattering properties of homogeneous nonspherical scatterers with the T-Matrix method. Requires NumPy and SciPy.',
    classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Fortran",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Physics",
        ],
    packages=['pytmatrix', 'pytmatrix.test', 'pytmatrix.quadrature', 'pytmatrix.fortran_tm'],
    package_data={
        'pytmatrix': ['ice_refr.dat'],
        'pytmatrix.fortran_tm': ['ampld.par.f']
    },

    # Install dependencies
    install_requires=['numpy', 'scipy'],

    # Custom build step
    cmdclass={
        'build_ext': PyTMatrixBuildExt,  # Use our custom build_ext that runs f2py
    },

    zip_safe=False,  # Avoid zip safe for binary extensions
)
