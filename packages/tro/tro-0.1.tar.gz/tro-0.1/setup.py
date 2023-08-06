from setuptools import setup,find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

# See https://setuptools.readthedocs.io/en/latest/setuptools.html
setup(name='tro',
	version='0.1',
	description='Best Dog',
	long_description=readme(),
	# Find classifiers at https://pypi.org/pypi?%3Aaction=list_classifiers
	# classifiers=[],
	# keywords='keywords-to-be-list',
	# scripts=['bin/run_scripts'],
	# entry_points = {
	# 'console_scripts': ['funniest-joke=funniest.command_line:main'],
	# }	
	url='https://github.com/fxie97/python-packaging-template',
	author='gerardnavarro22',
	author_email='gerard.navarro22@gmail.com',
	license='MIT',
	packages=find_packages(),
	# To copy all files listed in MANIFEST.in to site-packages
	include_package_data=True,
	zip_safe=False)

