from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 's4g',
    version = '0.0.1',
    author = 'Shubham Mishra',
    author_email = 'grapheo12@gmail.com',
    license = 'MIT',
    description = 'Stupid Simple Static Site Generator',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://gitlab.com/grapheo12/s4g',
    py_modules = ['s4g'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        s4g=s4g.__main__:main
    '''
)