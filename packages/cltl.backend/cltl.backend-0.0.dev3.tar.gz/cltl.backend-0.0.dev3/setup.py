from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setup(
    name='cltl.backend',
    version=version,
    package_dir={'': 'src'},
    packages=find_namespace_packages(include=['cltl.*', 'cltl_service.*'], where='src'),
    data_files=[('VERSION', ['VERSION'])],
    url="https://github.com/leolani/cltl-backend",
    license='MIT License',
    author='CLTL',
    author_email='t.baier@vu.nl',
    description='Backend for Leolani',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    install_requires=['numpy'],
    extras_require={
        "impl": [
            "mock",
            "requests",
            "parameterized"
        ],
        "host": [
            "cachetools",
            "pyaudio",
            "opencv-python",
            "flask"
        ],
        "service": [
            "cltl.combot",
            "emissor",
            "flask",
            "pyaudio",
            "requests",
            "sounddevice",
            "soundfile",
        ]
    }
)
