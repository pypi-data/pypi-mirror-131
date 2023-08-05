import codecs
import os.path
import setuptools
from setuptools import find_namespace_packages, find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
	name="dewloosh.math",
    version=get_version("src/Dewloosh/math/__init__.py"),                        
    author="dewloosh",
    author_email = 'dewloosh@gmail.com',                   
    description="A numerical math library for applications in various bramches of science and engineering",
    long_description=long_description,   
    long_description_content_type="text/markdown",
	url = 'https://github.com/dewloosh/dewloosh-math',   
    download_url = 'https://github.com/dewloosh/dewloosh-math/archive/refs/tags/0_0_dev5.zip', 
	packages=find_namespace_packages(where='src', include=['dewloosh.*']),
	classifiers=[
        'Development Status :: 3 - Alpha',     
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',
		'Operating System :: OS Independent'
    ],                                      
    python_requires='>=3.6',                             
    package_dir={'':'src'},     
    install_requires=required,
	zip_safe=False,
)

