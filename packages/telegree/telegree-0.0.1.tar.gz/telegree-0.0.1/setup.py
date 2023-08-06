import setuptools

requirements = ["aiogram<=2.17.1"]

setuptools.setup(
    name="telegree",
    version="0.0.1",
    author="Damir Stash",
    author_email="damirstash34@gmail.com",
    description="Python Module for creating telegram bots",
    packages=setuptools.find_packages(),
    install_requres=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7'
)