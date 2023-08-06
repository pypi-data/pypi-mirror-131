from setuptools import setup, find_packages

setup(
    name='MdsSoftwareSetup533',
    version='0.4',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A test python package',
	url='https://github.com/MayukhaB/Data533_Lab4.git',
    author='Mayukha Bheemavarapu',
    author_email='mayukhabheemavarapu@gmail.com',
    include_package_data=True,
    package_data={'': ['*.csv']}
    
)
