
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
#long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='kapa',  
    version='0.0.1', 
    description='Kinase Activity Profiling Analysis',  
    long_description="",
    long_description_content_type='text/plain', 
    author='Yao Gong', 
    author_email='gong0062@umn.edu',  

    classifiers=[  # Optional

        'Programming Language :: Python :: 3',
    ],


    keywords='python, phosphorylation, kinase, enrichment',  
    include_package_data=True,
    packages=find_packages(), 
#    package_dir={"": ""}, 

    python_requires='>=3.6, <4',


    install_requires=['numpy>1.16.2',
			'pandas>0.24.1',    
			'statistics',
			'scipy>1.6.1'],  

#    package_data={ "": ['unigenedict.csv','kindictgene.csv','kindictpro.csv'],},

#    project_urls={  
#        'Bug Reports': '',
#        'Funding': '',
#        'Say Thanks!': '',
#        'Source': '',
#    },
)

