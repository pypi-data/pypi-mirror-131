import setuptools

setuptools.setup(
    name="htlib",
    version="0.12",
    author="Harol Alvarado",
    author_email="harolav3@gmail.com",
    description="htlib package",
    url="https://github.com/harol1997/htlib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)