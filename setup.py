import os
import os.path
from setuptools import find_packages, setup
from pip._internal.req import parse_requirements
from track_api_client.constants import VERSION


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# parse_requirements() returns generator of pip.req.InstallRequirement objects
cur_dir = os.path.abspath(os.path.dirname(__file__))
install_reqs = parse_requirements(os.path.join(cur_dir, 'requirements.txt'), session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='track-api-client-py',
    version=VERSION,
    packages=find_packages(),
    description='Python client for track-api',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[],
    install_requires=reqs
)
