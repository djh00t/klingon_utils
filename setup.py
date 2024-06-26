from setuptools import setup, find_packages

setup(
    name="klingon_tools",
    version="0.0.33",  # This line will be updated dynamically by the Makefile
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "push=klingon_tools.push:main",
            "gh-actions-update=klingon_tools.gh_actions_update:main",
            "gh-pr-gen-title=klingon_tools.entrypoints:gh_pr_gen_title",
        ],
    },
    install_requires=[
        "openai",
        "argparse",
        "requests",
        "httpx",
        "pandas",
        "flask",
        "windows-curses; platform_system == 'Windows'",
        "watchdog",
        "pyyaml",
        "pytest",
    ],
    include_package_data=True,
    description="A set of utilities for running and logging shell commands in a user-friendly manner.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="David Hooton",
    author_email="klingon_tools+david@hooton.org",
    url="https://github.com/djh00t/klingon_tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
