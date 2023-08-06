from setuptools import setup, find_packages

setup(
    name='cryptlex_python_sdk',
    version='1.0.0',
    license='MIT',
    author="Ranjan P",
    author_email='ranjanp75@gmail.com',
    description="Cryptlex python client for Web APIs",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ranjanp75/cryptlex-python-sdk',
    keywords='Cryptlex Python client SDK ',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[l.strip() for l in open('requirements.txt').readlines()]
)
