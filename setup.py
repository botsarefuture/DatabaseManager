from setuptools import setup, find_packages

# Read the content of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="DatabaseManager",
    version="0.4.0",  # Incremented version
    packages=find_packages(),
    install_requires=[
        "pymongo>=3.11",  # Minimum version of pymongo
    ],
    description="A simple MongoDB manager package for Python applications.",
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify that the long description is in Markdown
    author="Verso Vuorenmaa",
    author_email="verso@luova.club",
    url="https://github.com/botsarefuture/DatabaseManager",  # Update with your repo link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Specify your license
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Development Status :: 4 - Beta",  # Indicate the development status
    ],
    python_requires='>=3.6',  # Specify the Python version requirement
    keywords="mongodb database manager python",  # Add relevant keywords
    project_urls={
        "Documentation": "https://github.com/botsarefuture/DatabaseManager/wiki",  # Documentation link
        "Source": "https://github.com/botsarefuture/DatabaseManager",  # Source code link
        "Tracker": "https://github.com/botsarefuture/DatabaseManager/issues",  # Issues link
    },
)
