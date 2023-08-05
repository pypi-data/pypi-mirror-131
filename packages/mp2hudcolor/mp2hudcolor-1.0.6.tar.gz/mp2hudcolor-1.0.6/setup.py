from pathlib import Path
from setuptools import setup, Extension
from Cython.Distutils import build_ext

src = [
    'mp2hudcolor/mp2hudcolor_wrapper.pyx'
]

extensions = [
    Extension("mp2hudcolor", src)
]

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mp2hudcolor",
    version="1.0.6",
    description="Modifies an existing NTWK file for Metroid Prime 2: Echoes and changing the color of the HUD.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toasterparty/mp2hudcolor",
    author="toasterparty",
    author_email="toasterparty@derpymail.org",
    license="MIT",
    packages=['mp2hudcolor'],
    install_requires=[
        'cython',
        'numpy',
    ],
    ext_modules=extensions,
    cmdclass={"build_ext": build_ext},
    package_data={'mp2hudcolor': ['mp2hudcolor.c']}
)
