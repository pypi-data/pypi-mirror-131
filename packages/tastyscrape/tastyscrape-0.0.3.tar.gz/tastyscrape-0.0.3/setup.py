from distutils.core import setup
import setuptools
setup(
  name = 'tastyscrape',
  packages=setuptools.find_packages(),
  version = '0.0.3',
  license='MIT',
  description_file = 'Scrape live option, stock, and futures data from tastyworks.',  
  author = 'Cliff Syner', 
  author_email = 'cragfintech@gmail.com',  
  url = 'https://github.com/c4syner/tastyscrape',
  download_url = 'https://github.com/c4syner/tastyscrape/archive/refs/tags/ts_v0.0.3.tar.gz',
  keywords = ['trading', 'stock', 'options'],
  install_requires=[
          'requests',
          'aiohttp',
          'aiocometd'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',    
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',  
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)