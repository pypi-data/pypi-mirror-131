from distutils.core import setup

setup(
  name = 'aiohttp-setup',
  packages = ['aiohttp-setup'],
  version = '0.1',
  license='MIT',
  description = 'A function for setting up aiohttp web server.',
  author = 'Михаил Беляков (Michael Belyakov)',
  author_email = 'bigbelk@live.ru',
  url = 'https://github.com/yababay/aiohttp-setup',
  download_url = 'https://github.com/yababay/aiohttp-setup/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['aiohttp', 'web server'],
  install_requires=[
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)
