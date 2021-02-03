import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hydroponics",
    version="0.0.1",
    author="John Oram",
    author_email="john@oram.ca",
    description="A small raspberry pi hydroponics setup.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joram/hydroponics",
    packages=[
        "Flask>=1.1.0",
        "Flask-SQLAlchemy",
        "flask_cors",
        "sqlite3",
        "sqlalchemy",
        "RPi.GPIO",
        "fake_rpi",
        "env",
        "PiPyADC",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
