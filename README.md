PyTMatrix-LTE
=========
A Python code for computing the scattering properties of homogeneous nonspherical scatterers with the _T_-Matrix method.\
Uses the [T-Matrix code by M. I. Mishchenko and L. D. Travis](http://www.giss.nasa.gov/staff/mmishchenko/t_matrix.html).

This is adapted from the original PyTMatrix code by Jussi Leinonen, which can be found [here](https://github.com/jleinonen/pytmatrix).\
It was adapted to run with newer versions of python (installation of the original code was buggy for python>3.6, fully deprecated for python>3.12).\
The adaptations include:
- Migration from distutils to setuptools (setup.py rewritten)
- Migration of certain scipy functions to new names


## Installation
The installation instructions in the original wiki are outdated and **do not** work for recent python versions (python>3.6).\
Use the following instructions instead (given for python 3.12, but should work for any python>3.6).
* Clone the repository: `git clone ...`
* Activate a conda environment with the following required packages: `numpy`, `scipy`, `meson`, `ninja`. You can create an appropriate environment with the following command: `conda create -n tmatrix python=3.12 numpy scipy meson ninja`
* In the terminal run the following commands:
```
cd pytmatrix-lte
python3 setup.py install
```
- The code should now be installed and ready to use.


## Usage
- See the [usage instructions](https://github.com/jleinonen/pytmatrix/wiki) in the original wiki.
- Simple testing - run the following in the chosen python environment but ***outside*** the pytmatrix-lte directory, otherwise this can mess up the imports:
 ```
    from pytmatrix.test import test_tmatrix
    test_tmatrix.run_tests() 
```

