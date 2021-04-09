from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name="tree-ops",
    version='0.0.0',
    license='MIT',
    author='M. H. Bani-Hashemian',
    author_email='hossein.banihashemian@alumni.ethz.ch',
    description='Processing large amount of data using tree and graph data structures.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seyedb/tree-ops',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    test_suite='tests',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=[],
    python_requires='>=3.6',
    install_requires=requirements
)
