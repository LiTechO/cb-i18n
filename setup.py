from setuptools import setup

setup(
    name = "cb_i18n",
    author = "weerdy15",
    url = "https://github.com/LiTechO/cb-i18n",
    project_urls = {
        "Issue tracker": "https://github.com/LiTech/cb-i18n/issues"
    },
    version = "1.0.3",
    packages = [
        "cb_i18n",
    ],
    license = "MIT",
    description = "Advanced internationalisation (i18n) support for Discord bots, originally developed for ClansBot",
    long_description = open('README.md', 'r').read(),
    long_description_content_type = "text/markdown",
    install_requires = [],
    extras_require = {},
    python_requires = ">=3.8.0",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ]
)
