import os
import io

from setuptools import setup, find_packages


def read(fname):
    with io.open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8") as f:
        return f.read()


setup(
    name="nnpackage",
    version="0.0.5",
    author="Alexander D. Kazakov",
    email="alexander.d.kazakov@gmail.com",
    url="https://github.com/AlexanderDKazakov/schnetpack/",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.1",
        "numpy",
        "ase>=3.18",
        "h5py",
        "tensorboardX",
        "tqdm",
        "pyyaml",
    ],
    extras_require={"test": ["pytest", "sacred", "pytest-console-scripts"]},
    license="MIT",
    description="NNPackage - Deep Neural Networks for Atomistic Systems (based on SchNetPack)",
    long_description="""
        NNPackage is a reduced version of SchNetPack for internal needs.""",
)
