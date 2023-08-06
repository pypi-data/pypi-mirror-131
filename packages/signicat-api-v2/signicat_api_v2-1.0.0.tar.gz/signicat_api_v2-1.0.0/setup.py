from distutils.core import setup

setup(
    name='signicat_api_v2',
    packages=['signicat_api_v2'],
    version='1.0.0',
    description='Rabobank Signicat API wrapper',
    author='Theo Bouwman',
    author_email='theo.bouwman@swishfund.nl',
    package_dir={'': 'src'},
    install_requires=[
        'requests==2.21.0'
    ],
    maintainer="Ugurcan Akpulat",
    maintainer_email="ugurcan.akpulat@swishfund.nl"
)