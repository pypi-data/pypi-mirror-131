from setuptools import find_packages, setup


with open('README.MD') as f:
    long_description = f.read()
    
setup(
    name='mpose',
    packages=find_packages(),
    version='1.0.6',
    description='MPOSE2021: a Dataset for Short-time Pose-based Human Action Recognition',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    author='Simone Angarano',
    license='MIT',
    install_requires=['numpy', 'tqdm', 'pyyaml', 'importlib_resources'],
    package_data={'': ["*.yaml"]}
)