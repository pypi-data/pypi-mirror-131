import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="arithmetic-goimoi", # Replace with your own username
    version="0.0.1",
    author="leminhdang",
    author_email="levangiau268@gmail.com",
    description="A simple arithmetic package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nguyennhattam268/ChatbotAI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)