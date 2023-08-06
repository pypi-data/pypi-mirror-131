from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
     name='ShynaSystemInfo',
     version='0.1',
     packages=find_packages(),
     author="Shivam Sharma",
     author_email="shivamsharma1913@gmail.com",
     description="Shyna Backend Functionality Package to fetch System information",
     long_description=long_description,
     long_description_content_type="text/markdown",
    )

install_requires = [
    'psutil',
    'os',
    "setuptools",
    "wheel",
    "urllib3"
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
