# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_mailman', 'fastapi_mailman.backends']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'aiosmtplib>=1.1.6,<2.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'email-validator>=1.1.3,<2.0.0',
 'fastapi>=0.68.1,<0.69.0',
 'pydantic>=1.8.2,<2.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=21.1,<22.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'mkdocs-material-extensions>=1.0.1,<2.0.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0',
          'anyio>=3.3.2,<4.0.0',
          'trio>=0.19.0,<0.20.0']}

setup_kwargs = {
    'name': 'fastapi-mailman',
    'version': '0.0.3',
    'description': "Porting Django's email implementation to your FastAPI applications.",
    'long_description': '# 📬 Fastapi-Mailman\n<img src="https://raw.githubusercontent.com/marktennyson/fastapi-mailman/master/logos/fastapi_mailman_logo.png"></img>\n\n### 🔥 Porting Django\'s email implementation to your FastAPI applications.\n![PyPI](https://img.shields.io/pypi/v/fastapi-mailman?color=blue)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-mailman?color=brightgreen)\n[![dev workflow](https://github.com/marktennyson/fastapi-mailman/actions/workflows/dev.yml/badge.svg?branch=master)](https://github.com/marktennyson/fastapi-mailman/actions/workflows/dev.yml)\n![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/marktennyson/fastapi-mailman/latest?color=cyan)\n![PyPI - License](https://img.shields.io/pypi/l/fastapi-mailman?color=blue)\n\nFastapi-Mailman is a Fastapi extension providing simple email sending capabilities. It\'s actually a hard fork of `waynerv\'s` `flask-mailman` module. I have tried to implement the same features for the `Fastapi` too.\n\nIt was meant to replace the basic Fastapi-Mail with a better warranty and more features.\n\n## ⛲ Key Features:\n1. Easy to use.\n2. Backend based email sender.\n3. Customisable backend class.\n4. Proper testcases.\n5. Proper documentation.\n\n## 🔗 Important Links:\n[Github Repo](https://github.com/marktennyson/fastapi-mailman)     \n[PYPI](https://pypi.org/project/fastapi-mailman)     \n[Documentation](https://marktennyson.github.io/fastapi-mailman)      \n\n## 💯 Usage\n\nFastapi-Mailman ported Django\'s email implementation to your Fastapi applications, which may be the best mail sending implementation that\'s available for python.\n\nThe way of using this extension is almost the same as Django.\n\nDocumentation: [https://marktennyson.github.io/fastapi-mailman.](https://marktennyson.github.io/fastapi-mailman)\n\n## \U0001fa9c Basic Example\n```python\nfrom fastapi import FastAPI\nimport uvicorn as uv\nfrom fastapi_mailman import Mail, EmailMessage\nfrom fastapi_mailman.config import ConnectionConfig\n\napp = FastAPI(debug=True)\n\nconfig = config = ConnectionConfig(\n    MAIL_USERNAME = \'example@domain.com\',\n    MAIL_PASSWORD = "7655tgrf443%$",\n    MAIL_BACKEND =  \'smtp\',\n    MAIL_SERVER =  \'smtp.gmail.com\',\n    MAIL_PORT = 587,\n    MAIL_USE_TLS = True,\n    MAIL_USE_SSL = False,\n    MAIL_DEFAULT_SENDER = \'example@domain.com\',\n    )\nmail = Mail(config)\n\n@app.get("/send-base")\nasync def send_base():\n    msg = EmailMessage(\'this is subject\', \'this is message\', to=[\'aniketsarkar@yahoo.com\'])\n    await msg.send()\n    return {"Hello": "World"}\n\n@app.get("/send-mail")\nasync def check_send_mail():\n    await mail.send_mail("this is subject", "this is message", None, ["aniketsarkar@yahoo.com"])\n    return {"Hello": "World"}\n\n\nif __name__ == "__main__":\n    uv.run(app, port=8082, debug=True)\n```\n## 🚇 Development\n\n#### 🧑\u200d💻 Contribution procedure.\n1. Create a new issue on github.\n2. Fork and clone this repository.\n3. Make some changes as required.\n4. Write unit test to showcase its functionality.\n5. Submit a pull request under the `master` branch.\n\n#### 🖨️ Run this project on your local machine.\nTo run this project on your local machine please [click here](https://marktennyson.github.io/fastapi-mailman/contributing)\n\n### ❤️ Contributors\nCredits goes to these peoples:\n\n<a href="https://github.com/marktennyson/fastapi-mailman/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=marktennyson/fastapi-mailman" />\n</a>\n\n## 📝 License\n\nGNU General Public License v3 or later (GPLv3+)\n\nCopyright (c) 2021 Aniket Sarkar(aniketsarkar@yahoo.com)\n',
    'author': 'Aniket Sarkar',
    'author_email': 'aniketsarkar@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marktennyson/fastapi-mailman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
