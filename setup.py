import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="journalmtpd",
    version="0.0.1",
    author="Alexander Boström",
    author_email="abo@kth.se",
    description="LMTP to Journal gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abokth/journalmtpd",
    packages=['journalmtpd', 'journalmtpd._private'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/journalmtpd'],
)
