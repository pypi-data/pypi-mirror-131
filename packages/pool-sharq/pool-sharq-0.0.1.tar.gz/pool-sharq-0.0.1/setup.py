# setup.py

__module_name__ = "setup.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# package imports #
# --------------- #
import os
import re
from setuptools import setup
import sys


setup(
    name="pool-sharq",
    version="0.0.1",
    python_requires=">3.7.0",
    author="Michael E. Vinyard - Harvard University - Massachussetts General Hospital - Broad Institute of MIT and Harvard",
    author_email="mvinyard@broadinstitute.org",
    url="https://github.com/mvinyard/pool-sharq",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="pool-sharq: python interface for Broad Institute GPP's poolq software.",
    packages=[
        "pool_sharq",
    ],
    install_requires=[
        "beautifulsoup4>=4.10.0",
        "licorice>=0.0.2",
        "pandas>=1.3.4",
        "pyrequisites>=0.0.2",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
