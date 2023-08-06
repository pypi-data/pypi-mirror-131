import pathlib
from setuptools import find_packages, setup


HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='BreathFinder',
    long_description=README,
    packages=find_packages(include=['BreathFinder','numpy', 'sklearn', 'scipy']),
    
    long_description_content_type="text/markdown",
    install_requires=[
          'numpy',
          'sklearn',
          'scipy'
    ],
    version='0.2.1',
    url="https://github.com/benedikthth/BreathFinder",
    description='''Algorithm designed to find locations of
    individual breaths in a PSG''',
    author='Benedikt Holm Thordarson',
    author_email="b@spock.is",
    license='MIT',
)
print("~~~~~~~~~~~~~~~~~~")