from setuptools import setup, find_packages


def read_file(file: str):
    try:
        with open(file) as fh:
            return fh.read()
    except FileNotFoundError:
        return ""


def parse_requirements(file: str):
    try:
        with open(file) as fh:
            return [r.strip("\n") for r in fh.readlines() if not r.startswith("-")]
    except FileNotFoundError:
        return ""


LICENSE = read_file("LICENSE")
README = read_file("README.md")
CHANGELOG = read_file("CHANGELOG.md")
setup(
    name='savory',
    version='0.1.4',
    description='cli tool to manage saltstack git repositories',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("requirements-dev.txt"),
    url='https://gitlab.com/solvinity/savory',
    author='Solvinity',
    author_email='shared-services@solvinity.com',
    license='MIT',
    package_data={'': ['LICENSE', 'README.rst', 'CHANGELOG.rst']},
    packages=['savory'],
    scripts=['bin/savory'],
    classifiers=[],
    test_suite="tests",
    zip_safe=True,
    include_package_data=True,
)
