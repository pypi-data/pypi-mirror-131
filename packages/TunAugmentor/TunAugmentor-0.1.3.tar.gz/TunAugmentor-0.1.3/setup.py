from setuptools import find_packages,setup

setup(
    name='TunAugmentor',
    packages=find_packages(include=['TunAugmentor']),
    version='0.1.3',
    description='Python library for image data augmentation',
    author='Ahmed Belgacem, Firas Meddeb',
    author_email = 'ahmedbelgaacem@gmail.com',
    url="https://github.com/ahmedbelgacem/TunAugmentor",
    download_url ="https://github.com/ahmedbelgacem/TunAugmentor/archive/refs/tags/0.1.2.tar.gz",
    license='MIT',
    install_requires=['numpy','opencv-python'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)
