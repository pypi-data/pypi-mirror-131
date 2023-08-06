from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pyTextColor',
    version='1.0.1',
    description='Simple Python Library to display text with color in Python Terminal!',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Sid72020123/pyTextColor/',
    author='Siddhesh Chavan',
    author_email='siddheshchavan2020@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='color-outputs color text styling',
    packages=find_packages(),
    install_requires=[]
)
