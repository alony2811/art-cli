from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='artcli',
    version='0.1.0',
    description='API CLI to manage an Artifactory SaaS instance',
    log_description=readme,
    author='AlonYaron',
    author_email='alony@jfrog.com',
    install_requires=[],
    packages=find_packages('src'),
    package_dir={'': 'src'},
<<<<<<< HEAD
)
=======
)
>>>>>>> 70ad0cd0b65b652541b4660cc5bb7de603bea3ca
