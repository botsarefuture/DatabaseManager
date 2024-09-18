from setuptools import setup, find_packages

setup(
    name="DatabaseManager",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "pymongo"
    ],
    description="A simple MongoDB manager package",
    author="Verso Vuorenmaa",
    author_email="verso@luova.club",
    url="https://github.com/botsarefuture/DatabaseManager",  # Update with your repo link
)
