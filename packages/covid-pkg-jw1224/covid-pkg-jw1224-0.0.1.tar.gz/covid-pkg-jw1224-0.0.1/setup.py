import setuptools

VERSION = '0.0.1' 
DESCRIPTION = 'A package for displaying a Covid-19 dashboard.'
LONG_DESCRIPTION = 'This package takes data from both a Covid-19 and News API in order to display onto a webpage that can be continually updated.'


setuptools.setup(

        name="covid-pkg-jw1224", 
        version=VERSION,
        author="Jake Wakefield",
        author_email="jw1224@exeter.ac.uk",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=setuptools.find_packages(),

        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
)