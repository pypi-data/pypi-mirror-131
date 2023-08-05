import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    
    long_description = fh.read()
    
    setuptools.setup(
    
    name="csv_converter_and_book_recommender_pkg-Preeti_Rawat",
    # Replace with your own username above
    version="0.0.5",
    author="Preeti_Rawat",
    author_email="x20233507@student.ncirl.ie",
    description="A model to csv converter and book recommender package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/bookrecommenderandcsvconverter",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[''],
    classifiers=[
        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
