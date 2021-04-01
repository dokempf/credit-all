from setuptools import setup, find_packages


setup(
    name='creditall',
    version='0.0.1',
    url='https://github.com/dokempf/creditall.git',
    #author='Author Name',
    #author_email='author@gmail.com',
    #description='Description of my package',
    packages=find_packages(),    
    install_requires=[
        "click",
        "click-default-group",
        "jinja2",
    ],
    include_package_data=True,
)
