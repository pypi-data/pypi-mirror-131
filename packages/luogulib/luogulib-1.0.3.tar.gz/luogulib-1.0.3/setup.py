import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name='luogulib',
  version='1.0.3',
  author='Qin Yuzhen',
  author_email='15166054530@163.com',
  description='A python module for using Luogu API.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://gitee.com/cyoi-group/luogu-lib',
  packages=setuptools.find_packages(),
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Intended Audience :: Information Technology',
      'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
      'Natural Language :: Chinese (Simplified)',
      'Operating System :: MacOS',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3',
      'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  install_requires=[
        'bs4',
        'requests',
        'functoolsplus'
    ]
)