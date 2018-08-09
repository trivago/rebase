import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class Pytest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '--cov=rebase', '--cov-report', 'term-missing', '--fulltrace',
            '-vv', '-s'
        ]

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='rebase',
    version='1.2.2',
    python_requires='>=3.6',
    author="Yuv Joodhisty",
    author_email="locustv2@gmail.com",
    maintainer="Yuv Joodhisty",
    maintainer_email="locustv2@gmail.com",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'simplejson',
    ],
    tests_require=['pytest-cov', 'pytest', 'mock'],
    cmdclass={'test': Pytest},
    test_suite='tests',
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    )
)
