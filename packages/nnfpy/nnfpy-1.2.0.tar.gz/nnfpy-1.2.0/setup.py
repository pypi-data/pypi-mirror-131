from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='nnfpy',
    version='1.2.0',
    description='Neural network for python',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/sopho-s/nnfpy',
    author='Nick Woods, Olivier Hinds',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    author_email='woodsnicholas01@gmail.com',
    license='MIT',
    keywords='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[]
)
