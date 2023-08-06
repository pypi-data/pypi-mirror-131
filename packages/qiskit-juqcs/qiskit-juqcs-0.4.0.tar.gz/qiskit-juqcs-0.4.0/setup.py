import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='qiskit-juqcs',
      version='0.4.0',
      description="Qiskit provider for JUQCS (Juelich Universal Quantum Computer Simulator)",
      long_description=README,
      long_description_content_type='text/markdown',
      url='https://jugit.fz-juelich.de/qip/juniq-platform/qiskit-juqcs',
      author='Carlos Gonzalez',
      author_email='c.gonzalez.calaza@fz-juelich.de',
      license='MIT',
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"],
      packages=['juqcs'],
      install_requires=['pyunicore', 'numpy', 'qiskit>=0.23.0'],
      zip_safe=False)
