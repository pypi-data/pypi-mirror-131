from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'stock market, mutual funds, commodities and general investments'
LONG_DESCRIPTION = 'Mokola is a python package that enables users to get data on stock market accross West Africa'
HOMEPAGE= 'https://github.com/makkasbed/mokola'
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="mokola", 
        version=VERSION,
        author="Adu Bediako Asare",
        author_email="adu.asare@logiclabent.com",
        description=DESCRIPTION,
        url=HOMEPAGE,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["bs4","pandas","numpy","matplotlib","requests"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'mokola','stocks','africa','ghana','nigeria','mutual funds','investments','commodities','pension funds'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Financial and Insurance Industry",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)