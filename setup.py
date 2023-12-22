from setuptools import setup, find_packages

setup(
    name='tech-solutions-utilities',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A utility library for database, SFTP, and Datadog API management',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
        'pandas',
        'paramiko',
        'trino',
        'datadog-api-client',
        'aiosonic',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
