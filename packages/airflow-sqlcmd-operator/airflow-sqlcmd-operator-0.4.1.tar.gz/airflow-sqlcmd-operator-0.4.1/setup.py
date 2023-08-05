import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name = 'airflow-sqlcmd-operator',         
    packages = ['airflow_sqlcmd_operator'],   
    version = '0.4.1',      
    license='MIT',        
    description = 'Custom Airflow BashOperator for Microsoft sqlcmd',
    long_description=README,
    long_description_content_type="text/markdown",
    author = 'Rodrigo Dewes',                   
    author_email = 'rdewes@gmail.com',      
    url = 'https://github.com/dewes/airflow-sqlcmd-operator',   
    download_url = 'https://github.com/dewes/airflow-sqlcmd-operator/archive/refs/tags/v_03.tar.gz',
    keywords = ['Airflow', 'operator', 'SQLServer', 'sqlcmd'],   
    install_requires=[
            'apache-airflow>=2.1',            
        ],
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    ],
)