from setuptools import setup

VERSION = '0.0.11'
DESCRIPTION = 'Control ilo robot using python command.'
LONG_DESCRIPTION = 'A package that allows user to control ilo the new education robot using python line command.'

# Setting up
setup(
    name="ilo",
    version=VERSION,
    author="ilo robot (SLB)",
    author_email="<ilotherobot@gmail.com>",
    url="https://github.com/ilorobot/python-library",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    py_modules=["ilo"],
    package_dir={'':'libname'},
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)