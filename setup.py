from setuptools import setup, find_packages

# Read the content of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="DatabaseManager",
    version="0.5.0",  # Incremented version
    packages=find_packages(),
    install_requires=[
        "pymongo>=3.11",  # Minimum version of pymongo
    ],
    description="A simple and efficient MongoDB manager package for Python applications.",
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify that the long description is in Markdown
    author="Verso Vuorenmaa",
    author_email="verso@luova.club",
    url="https://github.com/botsarefuture/DatabaseManager",  # Update with your repo link
    classifiers=[
        "Programming Language :: Python :: 3.7",  # Updated Python version requirement
        "License :: OSI Approved :: MIT License",  # Specify your license
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Development Status :: 4 - Beta",  # Indicate the development status
    ],
    python_requires='>=3.7',  # Specify the updated Python version requirement
    keywords="mongodb database manager python pymongo",  # Added more relevant keywords
    project_urls={
        "Documentation": "https://github.com/botsarefuture/DatabaseManager/wiki",  # Documentation link
        "Source": "https://github.com/botsarefuture/DatabaseManager",  # Source code link
        "Tracker": "https://github.com/botsarefuture/DatabaseManager/issues",  # Issues link
        "Changelog": "https://github.com/botsarefuture/DatabaseManager/releases",  # Changelog link
    },
)
