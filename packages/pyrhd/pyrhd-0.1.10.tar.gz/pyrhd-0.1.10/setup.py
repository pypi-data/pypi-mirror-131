import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrhd",
    version="0.1.10",
    author="abhira0",
    author_email="abhira0@protonmail.com",
    description="Scraping Library for Personal Use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/abhira0/pyrhd",
    project_urls={
        "URL Shortener": "https://abhirao.in/sh/",
        "Author Website": "https://abhirao.in",
        "GitHub": "https://github.com/abhira0/pyrhd",
    },
    # download_url="https://github.com/abhira0/pyrhd/archive/refs/tags/v0.1.3.zip",
    keywords=[
        "python",
        "scrape",
        "scraping",
        "scraper",
        "downloader",
        "python-scraper",
        "harvester",
        "harvest",
    ],
    license="MIT",
    packages=setuptools.find_packages(),
    # packages=["pyrhd"],
    install_requires=["requests", "bs4", "sty"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
