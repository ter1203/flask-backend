from setuptools import setup, find_packages

setup(
    name='fithm-gateway',
    version='1.1.0',
    description='Flask based api gateway to fithm service',
    author='Ryeland Gongora',
    author_email='rsgmon@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://www.fithm.com',
	install_requires=['Flask==2.0.1', 'SQLAlchemy==1.4.25', 'gunicorn==20.1.0', 'requests==2.26.0']
)
