from setuptools import find_packages, setup
import os



setup(name='zapy',
      version='0.0.11',
      description='OWASP ZAP Proxy API python package',
      author='midnight_repo',
      author_email='midnight_repo@protonmail.com',
      license='GPL-3.0',
      url='https://github.com/midnight-repo/ZAPY',
      packages=find_packages(),
      install_requires = ['beautifulsoup4', 'pandas', 'termcolor', 'requests', 'reindent']
      )
