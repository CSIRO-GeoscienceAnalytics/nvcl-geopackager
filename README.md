# nvcl-geopackager
A python project to assist with the creation and distribution of geopackage files to assist with geospatial searching.

# Problem 

There are known to be high quality geoscience data collections in the public domain which may be of interest to many geoscientists which are not easily discoverable.

These data collections may contain datapoints measured using a variety of different geoscience disciplines (eg. hyperspectral, geochemistry, text publications/reports, petrophysics etc..).

Having multidisciplinary data for a given location gives a collection additional research value over a dataset that may only cover a single discipline.

The AVRE supports data discovery but is more commonly used for specific types of data (drill holes, raster images, etc..) and which these more general collections do not easily fit into. 

Although the AVRE contains many layers and datasets, the process for adding new layers is convenient to geoscientists and typically requires specialist skills to perform. 

This project aims to assist in making these datasats more findable and accessible.

# Solution

This project aims to assist users in defining simple layer that can a be used to describe a generic data collection and provide a simple process that a researcher can follow to help them prepare a collection for publishing as a layer on a compatiable mapping portal such as AuScope AVRE.

# Documentation

# Usage
## Setup Environment

With python >3.6 installed the use of poetry is recommended to help manage the python environment.


Install poetry using pip:

```bash
> pip install poetry
```

then create a virtual python with all the required dependancies using poetry:

```bash
> poetry install
```
### Notebook
To run the notebook some additional setup steps are required:

```
> poetry run jupyter labextension install @pyviz/jupyterlab_pyviz
```

then run an instance of jupyer lab:

```bash
> poetry run jupyter lab
```

From within Jupyter lab open 'geopackager.ipynb'
