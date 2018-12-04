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
    2. [bokeh](https://bokeh.pydata.org/en/latest/): Run `pip install boken`
    3. [colorcet](https://colorcet.pyviz.org/): Run `pip install colorcet`
    4. [powerlaw](https://pypi.org/project/powerlaw/): Run `pip install powerlaw`
2. Run one of the following scripts
    - `python checkSQL.py`
    - `python fireMap.py > fireMap.csv`
    - `python sizeBucket.py > sizeBucket.csv`
    - `python contourMap1.py`

### Running from Jupyter/Anaconda

1. Install [Anaconda](https://www.anaconda.com/)
2. Run `conda install bokeh` in Anaconda Console
3. Run `conda install -c bokeh colorcet` in Anaconda Console
4. Run scripts with Jupyter

## Some useful links

- https://www.kaggle.com/rtatman/188-million-us-wildfires/kernels
- https://www.kaggle.com/katiej277/sqlite-in-python-intro
- http://tuvalu.santafe.edu/~aaronc/powerlaws/
