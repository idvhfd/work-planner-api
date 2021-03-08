import os
from setuptools import find_packages, setup

data_files = []

data_directories = ['migrations']
data_destination_dir = 'lib/planner-api'

for data_dir in data_directories:
    data_files += [(os.path.join(data_destination_dir, root), [os.path.join(root, f) for f in files])
        for root, dirs, files in os.walk(data_dir)]

setup(
    name='planner',
    version='0.1',
    packages=find_packages(),
    description='',
    scripts=['manage.py'],
    include_package_data=True,
    zip_safe=False,
    data_files=data_files,
)
