from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.23'
DESCRIPTION = "BUGGY ALPHA STATE"
LONG_DESCRIPTION = """Nope.
                    """

# Setting up
setup(
    name="tinda",
    version=VERSION,
    author="(Hank Singh)",
    author_email="<hanksingh07@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'argparse', 'wave', 'pyautogui', 'twine', 'pyttsx3', 'pyaudio', 'speedtest-cli', 'pynput', 'datetime', 'bs4', 'SpeechRecognition' ],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
