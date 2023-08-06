import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='scordt',
     version='0.1.2',
     author="Augusto Borges",
     author_email="borges.augustoar@gmail.com",
     description="Package to simplify the analysis of cilindrical-like \
      biological structures. Tailored specifically for axolotl spinal cord.",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://sysbioiflysib.files.wordpress.com/",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
