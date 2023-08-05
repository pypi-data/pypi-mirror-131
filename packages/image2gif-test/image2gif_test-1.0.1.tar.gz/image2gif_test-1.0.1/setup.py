from setuptools import setup, find_packages

setup(
    name             = 'image2gif_test',
    version          = '1.0.1',
    description      = 'Test package for distribution',
    author           = 'ChangGeun Oh',
    author_email     = 'fiveroot4@gmail.com',
    url              = '',
    download_url     = '',
    install_requires = ['pillow'],
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['GIFCONVERTER', 'gifconverter', 'image2gif'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
) 