from setuptools import setup, find_packages

setup(
    name='selection_sort',
    version='0.0.3',
    packages=find_packages(),
    author='Jiro1703',
    author_email='absurd4657@mail.ru',
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': [
            'selection_sort=selection_sort:main'
            'selection_sort.py=selection_sort:main'
        ]
    }
)
