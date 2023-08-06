import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="psgcompiler",
    version="1.5.1",
    author="PySimpleGUI",
    author_email="PySimpleGUI@PySimpleGUI.org",
    description="Convert your PySimpleGUI or other Python program into binary for easy distribution.  GUI uses PySimpleGUI. Back-end compile performed using pyinstaller (so far... others are being added)",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/PySimpleGUI/psgcompiler",
    packages=['psgcompiler'],
    install_requires=['PySimpleGUI>=4.55.1', 'PyInstaller'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Software Development :: Compilers",
        "Topic :: System :: Software Distribution",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ],
    package_data={"":["*.ico", "*.png"]},
    entry_points={
        'gui_scripts': [
            'psgcompiler=psgcompiler.psgcompiler:main'
        ],
    },
)
