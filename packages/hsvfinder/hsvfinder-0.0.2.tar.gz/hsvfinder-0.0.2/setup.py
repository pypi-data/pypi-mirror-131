from setuptools import setup, find_packages

setup(
    name="hsvfinder",
    version="0.0.2",
    author="Dan MacLean, Alexander Reynolds",
    python_requires='>=3.6',
    author_email='dan.maclean@tsl.ac.uk',
    install_requires=["opencv-python"],
    url="https://github.com/danmaclean/hsvfinder",
    packages=find_packages(),
    description="Reporting HSV values in flood filled masked areas.",
)
