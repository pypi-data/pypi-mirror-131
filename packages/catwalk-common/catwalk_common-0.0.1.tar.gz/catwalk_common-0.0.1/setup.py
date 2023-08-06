import setuptools

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="catwalk_common",
    description="Common code used in catwalk project",
    version='0.0.1',
    author_email='noreply@erst.dk',
    author='ERST',
    license='GPLv3+',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
    ],
    python_requires='>=3.8.0',
    install_requires=install_requires,
    dependency_links=[],
)
