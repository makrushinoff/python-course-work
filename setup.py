import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cw",
    version="0.1",
    description="python project",
    long_description="python project for course work",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "Django",
        "bcrypt",
        "djangorestframework",
        "djangorestframework-simplejwt",
        "django-cors-headers",
        "psycopg2-binary",
    ],
    python_requires=">=3.6",
)