import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='gerrit_coverage',
    url='https://github.com/tom-010/gerrit_coverage',
    version='0.0.4',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['gerrit_coverage'], # find_packages(),
    license='Apache2',
    install_requires=[
        'gerrit-robo==0.0.2',
        'missing-diff-lines==0.0.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='Convert the test-coverage-result while only including not covered lines in the current diff.',
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    include_package_data=True,
    entry_points = {
        'console_scripts': ['gerrit_coverage = gerrit_coverage:main'] 
    },
)