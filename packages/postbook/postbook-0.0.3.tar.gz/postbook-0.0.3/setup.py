import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="postbook", 
    version="0.0.3",
    author="Aswin Rajasekharan",
    author_email="aswin4400@gmail.com",
    description="Convert IPython Notebook to Blog Post",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aswin4400/postbook.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'nbconvert>=6.3.0',
        'typer>=0.4.0',
        'Jinja2>=3.0.3',
        'paramiko>=2.8.1',
        'nbformat>=5.1.3'
    ],
    python_requires='>=3.6',
    package_data={'postbook': ['templates/*','templates/aswins/*','templates/aswins/static/*',\
        'templates/classic/*','templates/classic/static/*','templates/base/*','templates/base/static/*']},
    entry_points={
        'console_scripts': [
            'postbook=postbook.main:main',
        ]
    }
)