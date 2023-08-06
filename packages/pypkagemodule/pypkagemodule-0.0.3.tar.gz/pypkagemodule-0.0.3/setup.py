from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="pypkagemodule",
    version=VERSION,
    author="Fred Chen",
    author_email="elastos.chen.yufei@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    # package_dir={"": "src"},
    # packages=find_packages(where='src'),

    # package是针对目录而言的，module是针对文件而言的
    packages=['src', 'src.extra'],
    py_modules=['manage', ],

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
