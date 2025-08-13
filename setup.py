from setuptools import setup

APP = ['main.py']
DATA_FILES = []  # Add 'icon.png' here once you have it
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # This makes it a status bar app without a dock icon
    },
    'packages': ['rumps', 'requests', 'pandas', 'numpy', 'datetime'],  # Include all required packages
}

setup(
    app=APP,
    name='VN-Index',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['rumps', 'vnstock', 'requests']
)
