import setuptools

setuptools.setup(
    name="RV8803",
    version="0.0.2",
    author="Tran Anh Nguyen",
    author_email="nguyenta@umich.com",
    description="A small package for using the RV8803 real time clock via I2C",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
