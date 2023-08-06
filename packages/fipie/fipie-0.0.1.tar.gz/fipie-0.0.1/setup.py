from setuptools import setup

setup(name='fipie',
      version='0.0.1',
      description='A simple portfolio optimiser beyond the mean-variance optimisation',
      long_description='',
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Office/Business :: Financial :: Investment',
      ],
      keywords='finance investment optimisation',
      url='https://github.com/thoriuchi0531/fipie',
      author='thoriuchi0531',
      author_email='thoriuchi0531@gmail.com',
      license='MIT',
      packages=['fipie'],
      install_requires=[
          'pandas>=0.25',
          'scipy>=1.0'
      ],
      extras_require={
          'dev': [
              'pytest',
              'coverage',
              'sphinx==4.2.0',
              'sphinx-book-theme==0.1.6',
              'myst_parser==0.15.2'
          ],
      },
      zip_safe=False,
      include_package_data=True,
      python_requires='>=3.6',
      )
