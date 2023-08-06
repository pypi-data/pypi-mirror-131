from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = long_description

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="pypkagemodule",
    version=VERSION,
    author="Fred Chen",
    author_email="elastos.chen.yufei@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    # all python modules are in pypkgmodule folder
    # package_dir={"": "pypkgmodule"},
    # # packages=find_packages(where='pypkgmodule', exclude=('tests', )),
    # packages=find_packages(where='pypkgmodule'),

    # package是针对目录而言的，module是针对文件而言的, 此配置导入包的时候会很乱，变成多个包
    # packages=['pypkgmodule', 'pypkgmodule.src'],
    # py_modules=['manage', ],

    # packages=find_packages(where='pypkgmodule'),
    packages=find_packages(exclude=('pypkgmodule.tests', )),

    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
