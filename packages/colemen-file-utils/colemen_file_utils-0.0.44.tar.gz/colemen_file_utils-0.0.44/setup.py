from setuptools import setup, find_packages

VERSION = '0.0.44'
DESCRIPTION = 'Colemen File Utils'
LONG_DESCRIPTION = 'Colemen File Utils'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="colemen_file_utils",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=['colemen_file_utils', 'utils.dir', 'utils.file_read', 'utils.file_search', "utils.file_write", "utils.file", "utils.objectUtils", "utils.string_utils"],
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'secure_delete',
        'ftputil',
        'colemen_string_utils'
    ],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
