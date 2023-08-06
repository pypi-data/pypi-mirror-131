import setuptools

setuptools.setup(
    name="aisy_database",
    version="0.2.0",
    author="Guilherme Perin",
    author_email="guilhermeperin7@gmail.com",
    description="Database Package for AISY Framework",
    long_description="# Database package to support AISY Framework \n"
                     
                     "pip install aisy-sca\n"
                     "pip install aisy-database\n"

                     "If you use our framework, please consider citing:\n"

                     "    @misc{AISY_Framework,"
                     "      author = {Guilherme Perin and Lichao Wu and Stjepan Picek},"
                     "      title  = {{AISY - Deep Learning-based Framework for Side-Channel Analysis}},"
                     "      howpublished = {AISyLab repository},"
                     "      note   = {{\\url{https://github.com/AISyLab/AISY_Framework}}},"
                     "      year   = {2021}"
                     "   }",
    long_description_content_type='text/markdown',
    keywords="side-channel analysis deep learning profiled attacks",
    packages=['aisy_database', 'tests'],
    url="https://aisylab.github.io/AISY_docs/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"]
)
