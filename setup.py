import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='markov-text-generator',
    version='0.0.1',
    author='Saul Johnson',
    author_email='saul.a.johnson@gmail.com',
    description='A quick Python implementation of a text generator based on a Markov process.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lambdacasserole/markov-text-generator.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
