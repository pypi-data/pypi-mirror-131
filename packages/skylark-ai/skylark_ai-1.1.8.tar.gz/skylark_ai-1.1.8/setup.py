import setuptools

setuptools.setup(
    name='skylark_ai',
    version='1.1.8',
    description='Websocket SDK for Skylark APIs',
    url='https://github.com/skylarklabsAI/python-sdk',
    author='skylarklabs',
    author_email='admin@skylarklabs.ai',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'websockets',
        'sockets',
        'asyncio',
        'threaded',
        'opencv-python',
        'numpy',
    ]
)
