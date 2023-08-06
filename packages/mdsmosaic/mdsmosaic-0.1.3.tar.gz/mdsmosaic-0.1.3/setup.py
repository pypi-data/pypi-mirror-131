from setuptools import setup


def readme():
    with open("README.rst", mode="r", encoding="utf-8") as f:
        return f.read()


setup(name="mdsmosaic",
      version="0.1.3",
      description="Client utilities for the MOSAIC suite",
      long_description=readme(),
      url="https://hub.docker.com/u/mds4ul",
      author="Maximilian Jugl",
      author_email="jugl@hs-mittweida.de",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Topic :: Scientific/Engineering :: Information Analysis",
          "Topic :: Software Development :: Libraries",
          "Typing :: Typed"
      ],
      license="MIT",
      packages=["mdsmosaic"],
      install_requires=[
          "marshmallow",
          "zeep"
      ],
      zip_safe=False)
