import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='hello_python_world',
    version='0.0.9',
    author='Marcell Biemann',
    author_email='mbiemann@gmail.com',
    description='A Hello World Python module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mbiemann/hello-python-world',
    project_urls={
        'Bug Tracker': 'https://github.com/mbiemann/hello-python-world/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['hello_python_world'],
    python_requires='>=3.6',
    install_requires=[],
)
