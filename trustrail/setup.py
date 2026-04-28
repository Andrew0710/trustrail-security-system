from setuptools import setup, find_packages

setup(
    name="trustrail",
    version="0.1.0",
    description="Shift-Left Security ecosystem to prevent sensitive data leaks",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.0",
        "djangorestframework>=3.14",
        "django-cors-headers>=4.0",
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'trustrail=trustrail.cli.main:main',
        ],
    },
)