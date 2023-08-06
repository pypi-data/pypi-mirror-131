import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

setup(
    name='cxr-service-client',
    version='0.0.3',
    description='CX Runner Service Client',
    long_description=(pathlib.Path(__file__).parent.resolve() / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/CiscoAandI/cxr_service_client',
    author='Ava Thorn',
    author_email='avthorn@cisco.com',
    classifiers=[
        'Topic :: Software Development :: Build Tools'
    ],
    keywords='cx, cx_runner, service, cisco',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'requests==2.26.0',
        'werkzeug==2.0.2'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/CiscoAandI/cxr_service_client/issues',
        'Source': 'https://github.com/CiscoAandI/cxr_service_client/',
    }
)
