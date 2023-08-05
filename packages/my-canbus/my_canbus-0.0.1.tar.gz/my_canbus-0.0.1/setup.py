from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='my_canbus',
  version='0.0.1',
  description='An application to get CAN bus info',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Jose Villa',
  author_email='ingenieria.htd@metgroupsas.com',
  license='MIT',
  classifiers=classifiers,
  keywords='CAN',
  packages=find_packages(),
  install_requires=['']
)
