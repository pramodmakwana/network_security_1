'''
The setup.py file is an essential part of packagina and distributing python projects
It is used by setuptools of the project , such as metadata, dependencies and more


'''
from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:  
    requirement_lst:List[str]=[]
    """
    THis fucntion will retrun list of requirements
    """
    try:
        with open ('requirements.txt','r')as file:
            # Read lineds from the file
            lines = file.readlines()
            #process each line
            for line in lines:
                requirement=line.strip()
                ##ignore empty lines and -e.
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requrirement file is not found") 
    return requirement_lst

setup(
    name="Networksecurity",
    version="0.0.1",
    author="Pramod Mawkana",
    author_email="pramod1117789@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
    )


