from os import path
from setuptools import setup, find_packages
with open(path.join(".", 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name="automate-graphite-feeder",
      version="0.9.1",
      description="A simple way to enrich with graphics the web interface for the automate-home projects",
      url="https://github.com/majamassarini/automate-home",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="Maja Massarini",
      author_email="maja.massarini@gmail.com",
      license="MIT",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3.8",
          "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
          "Intended Audience :: Developers",
      ],
      packages=find_packages(exclude=[]),
      include_package_data=True,
      install_requires=['automate-home'],
)
