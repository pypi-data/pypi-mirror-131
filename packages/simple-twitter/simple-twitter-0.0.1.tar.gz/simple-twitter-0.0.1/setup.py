import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simple-twitter',
    version='0.0.1',
    author='Marcell Biemann',
    author_email='mbiemann@gmail.com',
    description='A module to simplify the Twitter extraction',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mbiemann/simple-twitter',
    project_urls={
        'Bug Tracker': 'https://github.com/mbiemann/simple-twitter/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['simple_twitter'],
    python_requires='>=3.6',
    install_requires=[
        'requests==2.26.0'
    ],
)