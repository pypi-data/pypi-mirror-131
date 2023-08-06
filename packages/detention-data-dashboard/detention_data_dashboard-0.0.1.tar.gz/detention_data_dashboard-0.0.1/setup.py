import setuptools

setuptools.setup(
    name="detention_data_dashboard",
    version="0.0.1",
    author="Lucas Olson, Trung-Anh Nguyen, Maddie Gaumer",
    email="lkolson@uw.edu",
    description="a dashboard of ICE enforcement data",
    install_requires=['docutils>=0.3'],
    long_description="a dashboard that provides data on encounters, arrests, and removals by fiscal year between 2016-2019",
    long_description_content_type="text/markdown",
    url="https://github.com/detentiondatadashboard/detention_data_dashboard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
