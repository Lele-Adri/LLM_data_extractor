import os
from setuptools import find_packages
from setuptools import setup

requirements = []

if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as f:
        content = f.readlines()
    requirements.extend([x.strip() for x in content if 'git+' not in x])


setup(name='llm_extractor',
      version="0.0.1",
      description="Project Description",
      packages=find_packages(),
      install_requires=requirements,
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      # scripts=['scripts/ai-detector-run'],
      zip_safe=False)
