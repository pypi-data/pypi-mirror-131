import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='gerrit_review_robot',
    url='https://github.com/tom-010/gerrit_review_robot',
    version='0.0.4',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['gerrit_review_robot'],
    license='Apache2',
    install_requires=[
        'requests',
        'easy_exec'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='A framework for writing bots, that review a code base and post the review together with comments to Gerrit.',
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    include_package_data=True,
    entry_points={
    }
)