import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyautomouse",
    version="0.1.6",
    author="xiongtianshuo",
    author_email="seoul1k@163.com",
    url='https://github.com/seoul2k/pyautomouse',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/seoul2k/pyautomouse/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={".": "pyautomouse/"},
    install_requires=['pyautogui', 'time'],
    packages=setuptools.find_packages(),
    python_requires=">=2",
)
