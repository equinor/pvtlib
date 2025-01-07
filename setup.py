from setuptools import setup, find_packages

setup(
    name='pvtlib',
    version='1.0.0',
    author='Christian Hågenvik',
    author_email='chaagen2013@gmail.com',
    description='A library containing various tools in the cathegories of thermodynamics, fluid mechanics, metering etc.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chagenvik/pvtlib',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
