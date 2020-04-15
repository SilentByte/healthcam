from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="MaskCam",
    version="1.0.0",
    description="AWS Mask Detection Camera",
    long_description_content_type="text/markdown",
    url="TODO",
    author="Stephen Mott, Rico Beti",
    classifiers=["Development Status ::3 - Alpha",
                 "Intended Audience :: Developers",
                 "Topic :: Software Development :: AWS",
                 "Programming Language :: Python :: 3.7"],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires=">=3.5",
    platforms="Raspbian",
    entry_points={'console_scripts': [
        'MaskCam = maskcam.cli:cli'
    ]}
)
