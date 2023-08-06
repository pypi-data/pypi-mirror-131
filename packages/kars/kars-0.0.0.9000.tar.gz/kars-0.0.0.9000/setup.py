import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='kars',
      version='0.0.0.9000',
      url='https://gjhunt.github.io/kars/',
      author='Gregory J. Hunt',
      author_email='ghunt@wm.edu',
      description='Kernel Approximation to Raman Spectra',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='GPL3',
      packages=setuptools.find_packages(),
      install_requires=[
          'numpy',
          'scipy',
          ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Operating System :: OS Independent",
          'Topic :: Scientific/Engineering',
      ],
    zip_safe=True)
