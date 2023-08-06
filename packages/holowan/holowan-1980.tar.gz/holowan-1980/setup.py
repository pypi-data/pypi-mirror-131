import setuptools

setuptools.setup(name='holowan',
                 version='1980',
                 description='This is a Python SDK for HoloWAN',
                 author='chanyulin',
                 packages=setuptools.find_packages(),
                 package_data={"holowan": ["resources/*.xml", "resources/*.ini"]}
                 )
