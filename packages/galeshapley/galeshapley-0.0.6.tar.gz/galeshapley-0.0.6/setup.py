from setuptools import find_packages, setup
import pathlib

here=pathlib.Path(__file__).parent.resolve()
long_description=(here / 'README.md').read_text(encoding='utf-8')

setup(
    name='galeshapley',
    packages=find_packages(),
    version='0.0.6',
    description='Gale Shapley Algorithm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/stamps-group/galeshapley',
    author='Gomes, J.M.',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)