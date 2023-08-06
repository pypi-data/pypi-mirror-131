from setuptools import setup , find_packages

setup(
    name='lry_timer',
    version='0.0.4',
    description='this package is made by lry',
    #long_description=open('README.MD').read(),
    include_package_data=True,
    author='lry',
    author_email='1224137702@qq.com',
    maintainer='lry',       # 维护者
    maintainer_email='1224137702@qq.com',
    license='MIT LICENSE',
    url='https://github//lry-123456789',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.1',
    install_requires=['turtle'],
)