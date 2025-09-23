from setuptools import setup, find_packages

setup(
    name="st_polygoncluster",
    version="0.1.0",
    description="Spatio-temporal clustering for polygon geometries",
    author="Mykola Kozyr",
    packages=find_packages(),
    install_requires=[
        "geopandas",
        "shapely",
        "numpy",
        "scikit-learn",
        "hdbscan"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
