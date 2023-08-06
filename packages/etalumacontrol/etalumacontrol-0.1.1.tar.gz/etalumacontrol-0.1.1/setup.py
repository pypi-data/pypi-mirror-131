from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='etalumacontrol',
    version='0.1.1',
    description='Library for interacting with Etaluma microscopes and stages',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Jonas Ohlsson',
    author_email='jonas.ohlsson@slu.se',
    url='https://github.com/jonasoh/etalumacontrol',
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering",
    ],
    license="BSD license",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['intelhex>=2.3.0', 'Pillow>=8.3.1', 'pycparser>=2.20', 'pythonnet>=2.5.2', 'pyusb>=1.2.1']
)
