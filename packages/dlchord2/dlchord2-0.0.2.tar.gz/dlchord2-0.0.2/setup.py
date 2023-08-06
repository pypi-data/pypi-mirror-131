from setuptools import setup, find_packages
import sys

sys.path.append("./test/")
version = "0.0.2"

setup(
    name="dlchord2",
    version=version,
    description="chord library",
    install_requires=["numpy"],
    author="anime-song",
    url="https://github.com/anime-song/DLChord2",
    keywords='music chord',
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    test_suite='test',
)
