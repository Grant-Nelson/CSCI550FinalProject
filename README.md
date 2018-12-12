# CSCI 550 - Final Project

This is [Grant Nelson](https://github.com/Grant-Nelson) and [John Singleton](https://github.com/JohnSingleton54) final project at Montana State University 2019 for CSCI 550

## Getting Started

1. Download [FPA_FOD_20170508.sqlite](https://www.kaggle.com/rtatman/188-million-us-wildfires) data
    - If is zipped on download, unzip here
2. Install [Python](https://www.python.org/downloads/)
3. Then choose to run either Command Line or from Jupyter/Anaconda

### Running from Command Line

This method works for Linux and Mac. It also work for Windows if run from Visual Studio Code.

1. Install the following required packages:
    1. [numpy](https://scipy.org/install.html): Run `pip install numpy`
    2. [powerlaw](https://pypi.org/project/powerlaw/): Run `pip install powerlaw`
    3. The following packages are for the contourMap examples an may not work everywhere
        1. [bokeh](https://bokeh.pydata.org/en/latest/): Run `pip install boken`
        2. [colorcet](https://colorcet.pyviz.org/): Run `pip install colorcet`
2. Run one of the following scripts
    1. `python checkSQL.py`
    2. `python contourMap0.py > mapData.csv`
    3. `python contourMap1.py`
    4. `python contourMap2.py`
    5. `python contourMap3.py`
    6. `python contourMap4.py`
    7. `python contourMap5.py > mapData.csv`
    8. `python sizeBucket1.py > sizeBucket1.csv`
    9. `python sizeBucket2.py > sizeBucket2.csv`
    10. `python powerlawFull.py`
    11. `python powerlawByState.py > byState.csv`
    12. `python powerlawByYear.py > byYear.csv`
    13. `python compareFull.py`
    14. `python compareByState.py > compareByState.txt`
    15. `python compareByYear.py > compareByYear.txt`

### Running from Jupyter/Anaconda

1. Install [Anaconda](https://www.anaconda.com/)
2. Install the following required packages using the Anaconda console
    1. [bokeh](https://bokeh.pydata.org/en/latest/): Run `conda install bokeh`
    2. [colorcet](https://colorcet.pyviz.org/): Run `conda install -c bokeh colorcet`
    3. [powerlaw](https://pypi.org/project/powerlaw/): Run `conda install powerlaw`
3. Run scripts with Jupyter

## Some useful links

- https://www.kaggle.com/rtatman/188-million-us-wildfires/kernels
- https://www.kaggle.com/katiej277/sqlite-in-python-intro
- http://tuvalu.santafe.edu/~aaronc/powerlaws/
