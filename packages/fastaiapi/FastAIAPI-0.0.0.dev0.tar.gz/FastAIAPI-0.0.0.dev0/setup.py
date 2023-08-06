# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastaiapi']

package_data = \
{'': ['*']}

install_requires = \
['ASGIRef',
 'Auto-SKLearn>=0.14.2,<0.15.0',
 'Bayesian-Optimization>=1.2.0,<2.0.0',
 'CLICK',
 'Channels>=3.0.4,<4.0.0',
 'CloudPickle>=2.0.0,<3.0.0',
 'Colored>=1.4.3,<2.0.0',
 'ConfigSpace>=0.4.20,<0.5.0',
 'CoreAPI-CLI>=1.0.9,<2.0.0',
 'CoreAPI>=2.3.3,<3.0.0',
 'Daphne>=3.0.2,<4.0.0',
 'DataSets>=1.16.1,<2.0.0',
 'Django-MySQL>=4.3.0,<5.0.0',
 'FastAPI>=0.70.1,<0.71.0',
 'GUnicorn>=20.1.0,<21.0.0',
 'GitPython>=3.1.24,<4.0.0',
 'Google-Cloud-Translate>=3.6.1,<4.0.0',
 'GoogleTrans>=4.0.0rc1,<5.0.0',
 'GraphQL-Core>=3.1.6,<4.0.0',
 'GraphQL-Relay>=3.1.0,<4.0.0',
 'GraphQLClient>=0.2.4,<0.3.0',
 'Graphene>=3.0,<4.0',
 'HAL-Codec>=1.0.2,<2.0.0',
 'HTTPie>=2.6.0,<3.0.0',
 'Hpbandster>=0.7.4,<0.8.0',
 'HuggingFace-Hub>=0.2.1,<0.3.0',
 'Hypercorn>=0.12.0,<0.13.0',
 'JSONHyperSchema-Codec>=1.0.3,<2.0.0',
 'JSONSchema>=4.2.1,<5.0.0',
 'JobLib>=1.1.0,<2.0.0',
 'LIME>=0.2.0.1,<0.3.0.0',
 'MariaDB-DynCol>=3.4.0,<4.0.0',
 'Markdown>=3.3.6,<4.0.0',
 'MySQL-Connector-Python>=8.0.27,<9.0.0',
 'MySQLClient>=2.1.0,<3.0.0',
 'NumBa',
 'NumPy',
 'OpenAPI-Codec>=1.3.2,<2.0.0',
 'PSUtil>=5.8.0,<6.0.0',
 'Pandas>=1.3.4,<2.0.0',
 'Pillow>=8.4.0,<9.0.0',
 'PsycoPG2-binary>=2.9.2,<3.0.0',
 'Py-GQL>=0.6.1,<0.7.0',
 'PyArrow>=6.0.1,<7.0.0',
 'PySpark>=3.2.0,<4.0.0',
 'PyTZ>=2021.3,<2022.0',
 'Pydantic>=1.8.2,<2.0.0',
 'Python-DateUtil',
 'Python-DotEnv>=0.19.2,<0.20.0',
 'Quart>=0.16.1,<0.17.0',
 'Requests',
 'Ruamel.YAML>=0.17.17,<0.18.0',
 'S3FS>=2021.11.1,<2022.0.0',
 'SGQLC>=14.1,<15.0',
 'SQLAlchemy>=1.4.28,<2.0.0',
 'SQLModel>=0.0.5,<0.0.6',
 'SciKit-Fuzzy>=0.4.2,<0.5.0',
 'SciKit-Image>=0.19.0,<0.20.0',
 'SciKit-Learn',
 'SciPy',
 'SentencePiece>=0.1.96,<0.2.0',
 'Starlette',
 'StatsModels>=0.13.1,<0.14.0',
 'Tabulate>=0.8.9,<0.9.0',
 'TensorFlow-DataSets>=4.4.0,<5.0.0',
 'TensorFlow-Hub>=0.12.0,<0.13.0',
 'Torch-Model-Archiver>=0.5.0,<0.6.0',
 'TorchServe>=0.5.0,<0.6.0',
 'Tqdm>=4.62.3,<5.0.0',
 'Uvicorn>=0.16.0,<0.17.0']

extras_require = \
{':python_version < "3.10"': ['Ray>=1.9.0,<2.0.0',
                              'TensorFlow>=2.7.0,<3.0.0',
                              'Torch>=1.10.0,<2.0.0',
                              'TorchAudio>=0.10.0,<0.11.0',
                              'TorchText>=0.11.0,<0.12.0',
                              'TorchVision>=0.11.1,<0.12.0',
                              'Transformers>=4.12.5,<5.0.0',
                              'TIMM>=0.4.12,<0.5.0',
                              'Giotto-TDA>=0.5.1,<0.6.0',
                              'GUDHI>=3.4.1,<4.0.0',
                              'SHAP>=0.40.0,<0.41.0'],
 ':python_version < "3.9"': ['Kedro>=0.17.5,<0.18.0']}

setup_kwargs = {
    'name': 'fastaiapi',
    'version': '0.0.0.dev0',
    'description': 'FastAPI for Artificial Intelligence (AI) Applications',
    'long_description': '# FastAPI for Artificial Intelligence (AI) Applications\n',
    'author': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'author_email': 'Edu.AI@STEAMforVietNam.org',
    'maintainer': 'STEAM for Vietnam Foundation AI & Robotics Educational Initiative',
    'maintainer_email': 'Edu.AI@STEAMforVietNam.org',
    'url': 'https://GitHub.com/FastAIAPI/FastAIAPI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
