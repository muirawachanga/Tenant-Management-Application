from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tenantmanagementsystem/__init__.py
from tenantmanagementsystem import __version__ as version

setup(
	name="tenantmanagementsystem",
	version=version,
	description="Manage Tenant and Agents",
	author="Stephen",
	author_email="wachangasteve@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
