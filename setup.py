from setuptools import setup

setup(
    name="govinfo",
    version="0.0",
    author="Forest Gregg",
    author_email='fgregg@datamade.us',
    license="MIT",
    url="https://github.com/datamade/govinfo",
    packages=['govinfo'],
    description="A wrapper for the GPO's GovInfo API",
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=['scrapelib',
                      'pytz'],
)
