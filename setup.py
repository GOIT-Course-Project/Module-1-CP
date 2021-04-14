from setuptools import setup, find_namespace_packages

setup(
    name='personal_assistant',
    version='1.0.0',
    authors=('Volodymyr Dunkin', 'Andrii Mikhalkin'),
    description='personal assistant',
    entry_points={'console_scripts': [
        'assist = personal_assistant.general:main']},
    long_description='This application is intended for organizing, organizing and storing contacts and text notes',
    license='MIT license',

    packages=find_namespace_packages()
)
