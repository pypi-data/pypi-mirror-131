import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='report_not_covered_lines',
    url='https://github.com/tom-010/report_not_covered_lines',
    version='0.0.3',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['report_not_covered_lines'], # find_packages(),
    license='Apache2',
    install_requires=[
        'gerrit-review-robot',
        'not-covered-lines'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='Convert the test-coverage-result (saved in `.converage` to gerrit comments) while only including not covered lines in the current diff.',
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points = {
        'console_scripts': [
            'report_not_covered_lines = report_not_covered_lines:main',
        ] 
    },
)
