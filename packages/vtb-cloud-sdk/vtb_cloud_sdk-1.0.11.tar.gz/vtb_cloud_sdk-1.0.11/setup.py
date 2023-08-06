from setuptools import setup, find_packages

install_requires = [
    "requests",
    "python-dateutil",
    "docopt",
    "pytz",
    "beautifulsoup4",
    "lxml",
    "python-keycloak",
    "pyjwt",
    "logbook",
    "attrdict",
]

setup(
    name="vtb_cloud_sdk",
    version="1.0.11",
    packages=find_packages("."),
    install_requires=install_requires,
    url="https://bitbucket.region.vtb.ru/projects/PUOS/repos/cloud_sdk/",
    license="Private",
    author="Anton Tagunov",
    author_email="atagunov@asdco.ru",
    description="Client for VTB cloud",
    zip_safe=False
)
