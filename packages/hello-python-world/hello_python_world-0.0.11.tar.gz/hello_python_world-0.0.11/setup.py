import setuptools

_url = 'https://github.com/mbiemann/hello-python-world'

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
long_description = str(long_description) + '\n' + 'Check this project on GitHub: ' + _url

setuptools.setup(
    name='hello_python_world',
    version='0.0.11',
    author='Marcell Biemann',
    author_email='mbiemann@gmail.com',
    description='The Hello Python World module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=_url,
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
