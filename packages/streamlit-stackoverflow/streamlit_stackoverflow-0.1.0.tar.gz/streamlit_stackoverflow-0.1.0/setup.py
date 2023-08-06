# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_stackoverflow']

package_data = \
{'': ['*']}

install_requires = \
['streamlit>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-stackoverflow',
    'version': '0.1.0',
    'description': 'Project created to learning Streamlit.',
    'long_description': "# Stack Overflow Data Analysis\n[![GitHub][github_badge]][github_link] \n\nProject used to learning Streamlit.\n\n## Introduction\n\nLearning to use Streamlit to show charts with Pandas, ...\n\n### What this project can do\n\nThis project will help us to understand some information about Stack Overflow.\n\nThese questions will be answered:\n\n1. Percentagem of respondents who consider themseves professionals, non-professionals, students, hobbyists, etc.\n2. Distribution of respondents by location. Which country had the most participation?\n3. What is the respondent's distribution by level of education?\n4. What is the distribution of working time for each type of professional informed in question 1?\n5. Concerning people who work professionally:\n    1. What is their profession?\n    2. What is their level of education?\n    3. What is the company's size of those people who work professionally?\n6. The average salary of respondents?\n7. Using the top five countries that have the most respondents, what is the salary of these people?\n8. What is the percentage of people who work with Python?\n9. About python:\n    1. What is the salary level of people working with Python globally?\n    2. In Brazil, what is the salary level?\n    3. In the top five countries that have the most respondents, what is the salary level?\n10. Concerning all respondents, what operating system do they use?\n11. Concerning only people who work with Python, what operating system do they use?\n12. What is the average age of respondents?\n13. Concerning only people who work with Python, what is the average age?\n\nThis project is preferably installed with pipx:\n\n```bash\npipx install streamlit_stackoverflow\n```\n\nTo use, just type in:\n\n```bash\nxxxxxxxxxxxxxxxxx --help\n```\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/jpaulorc/streamlit_stackoverflow\n",
    'author': 'Joao Corte',
    'author_email': 'jpaulorc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
