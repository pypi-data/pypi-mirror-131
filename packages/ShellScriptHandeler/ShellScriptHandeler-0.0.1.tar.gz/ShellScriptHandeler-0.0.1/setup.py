from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Opens and runs Shellscripts'
LONG_DESCRIPTION = 'Allows you to Run and get the Output of Shellscripts'

# Setting up
setup(
    name="ShellScriptHandeler",
    version=VERSION,
    author="Teer2008 (Florian)",
    author_email="<henryzimmermann4@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'shellscript', 'sh', '.sh', 'run sh', 'open'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)