from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='funnypieces',
      version='0.1',
      description='The childhood memory about jigsaw puzzle game.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Image Processing :: Game',
      ],
      keywords='childhood memory about jigsaw puzzle game',
      url='http://github.com/manhdaovan/funnypieces',
      author='Manh DV',
      author_email='manhdaovan@gmail.com',
      license='MIT',
      packages=['funnypieces'],
      install_requires=[
          'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['pieces=funnypieces.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
