from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.1"
DESCRIPTION = "Сборник временных почтовых сервисов"
LONG_DESCRIPTION = Path(__file__).cwd().joinpath("README.md").read_text()


setup(
    name="mailmall",
    version=VERSION,
    author="Danil Krivoshapkin",
    author_email="deadcardinal293@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["httpx"],
    keywords=["python"],
)
