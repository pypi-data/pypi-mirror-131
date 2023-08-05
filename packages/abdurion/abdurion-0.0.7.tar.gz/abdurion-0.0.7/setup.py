import setuptools

# Loads your README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abdurion", # Replace with your own username
    version="0.0.7", # Your version number, needs to be incremented with each iteration
    author="Abdulrahman AlQumaidy", # Your name
    author_email="author@example.com", # Your email
    description="A small example package", # A one sentence description of your package
    long_description=long_description, # A longer description from your `README.md`
    long_description_content_type="text/markdown", # The format of you long_description file
    url="https://github.com/abdurion", # GitHub where to find your code
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Additional required pieces of metadata (Don't Change)
    packages=setuptools.find_packages(), # Find all packages used and get them ready for distribution (Dont Change)
    python_requires=">=3.7", # The required version of python
)