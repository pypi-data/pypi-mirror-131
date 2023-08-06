from setuptools import setup
from sys import platform

requirements = [
    'pyttsx3'
]

if platform == "win32":
    requirements.append('pypiwin32')

setup(
    name='workout.py',
    version='1.0.0',
    description='Workout buddy',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://www.devdungeon.com',
    author='DevDungeon',
    author_email='nanodano@devdungeon.com',
    license='GPL-3.0',
    py_modules=['workout'],
    entry_points={
        'console_scripts': [
            'workout = workout:main',
        ],
    },

    zip_safe=False,
    install_requires=requirements
)

