from setuptools import setup
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()
install_requires = install_requires

setup(
    name='drugs_graph',
    version='1',
    packages=['tests', 'drugs_graph', 'drugs_graph.src', 'drugs_graph.conf'],
    url='https://github.com/nbouml/drugs_graph',
    license='',
    author='noureddine',
    author_email='boum.nour19@gmail.com',
    description='',
    install_requires=install_requires
)
