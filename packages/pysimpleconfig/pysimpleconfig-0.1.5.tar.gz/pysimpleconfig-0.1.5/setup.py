from setuptools import find_packages, setup

try:
    from setupext_janitor import janitor
    CleanCommand = janitor.CleanCommand
except ImportError:
    CleanCommand = None

cmd_classes = {}
if CleanCommand is not None:
    cmd_classes['clean'] = CleanCommand

with open("README.md", "r") as fh:
    long_description = fh.read()

tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-pep8',
    'mock',
    'tox',
]

install_requires = [
    'extendable_json',
    'blinker'
]

setup_requires = [
    'pytest-runner',
    'sphinx'
]

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

version = "0.1.5"

setup(
    name='pysimpleconfig',
    version=version,
    release=version,
    author="Steven Swanson",
    author_email="Steven@SwanOhana.net",
    description="Simplified configuration file handler for any format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kiln707/simpleconfig",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    setup_requires=setup_requires,
    tests_require=tests_require,
    install_requires=install_requires,
    python_requires='>=3.6',
    cmdclass=cmdclass,
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'simpleconfig'),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'docs')}},
)
