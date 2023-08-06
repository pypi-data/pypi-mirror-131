# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bender',
 'bender.data_importer',
 'bender.data_importer.tests',
 'bender.evaluator',
 'bender.explorer',
 'bender.exporter',
 'bender.model_exporter',
 'bender.model_exporter.tests',
 'bender.model_loader',
 'bender.model_trainer',
 'bender.model_trainer.tests',
 'bender.pipeline',
 'bender.split_strategy',
 'bender.tests',
 'bender.trained_model',
 'bender.trained_model.tests',
 'bender.transformation',
 'bender.transformation.tests']

package_data = \
{'': ['*']}

install_requires = \
['aioaws>=0.12,<0.13',
 'asyncpg>=0.24.0,<0.25.0',
 'databases>=0.5.3,<0.6.0',
 'gspread>=4.0.1,<5.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'plotly>=5.3.1,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'seaborn>=0.11.2,<0.12.0',
 'sklearn>=0.0,<0.1',
 'xgboost>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'benderml',
    'version': '0.1.1',
    'description': 'A Python package that makes ML processes easier, faster and less error prone',
    'long_description': '# Bender 🤖\n\nA Python package for faster, safer, and simpler ML processes.\n\n## Why use `bender`?\n\nBender will make your machine learning processes, faster, safer, simpler while at the same time making it easy and flexible. This is done by providing a set base component, around the core processes that will take place in a ML pipeline process. While also helping you with type hints about what your next move could be.\n\n## Pipeline Safety\n\nThe whole pipeline is build using generics from Python\'s typing system. Resulting in an improved developer experience, as the compiler can know if your pipeline\'s logic makes sense before it has started.\n\nBender will therefore make sure you **can\'t** make errors like\n\n```python\n# ⛔️ Invalid pipeline\nDataImporters.sql(...)\n    .process([...])\n    # Compile Error: method `predict()` is not available\n    .predict()\n\n# ✅ Valid pipeline\nDataImporters.sql(...)\n    .process([...])\n    .load_model(ModelLoader.aws_s3(...))\n    .predict()\n```\n\n## Training Example\nBelow is a simple example for training a XGBoosted tree\n```python\nDataImporters\n    # Fetch SQL data\n    .sql(sql_url, sql_query)\n\n    # Preproces the data\n    .process([\n        # Extract advanced information from json data\n        Transformations.unpack_json("purchases", key="price", output_feature="price", policy=UnpackPolicy.median_number())\n\n        Transformations.log_normal_shift("y_values", "y_log"),\n\n        # Get date values from a date feature\n        Transformations.date_component("month", "date", output_feature="month_value"),\n    ])\n\n    # Split 70 / 30% for train and test set\n    .split(SplitStrategies.ratio(0.7))\n\n    # Train a XGBoosted Tree model\n    .train(\n        ModelTrainer.xgboost(),\n        input_features=[\'y_log\', \'price\', \'month_value\', \'country\', ...],\n        target_feature=\'did_buy_product_x\'\n    )\n\n    # Evaluate how good the model is based on the test set\n    .evaluate([\n        Evaluators.roc_curve(),\n        Evaluators.confusion_matrix(),\n        Evaluators.precision_recall(\n            # Overwrite where to export the evaluated result\n            Exporter.disk("precision-recall.png")\n        ),\n    ])\n```\n\n## Predicting Example\n\nBelow will a model be loaded from a AWS S3 bucket, preprocess the data, and predict the output.\nThis will also make sure that the features are valid before predicting.\n\n```python\nModelLoaders\n    # Fetch Model\n    .aws_s3("path/to/model", s3_config)\n\n    # Load data\n    .import_data(\n        DataImporters.sql(sql_url, sql_query)\n            # Caching import localy for 1 day\n            .cached("cache/path")\n    )\n    # Preproces the data\n    .process([\n        Transformations.unpack_json(...),\n        ...\n    ])\n    # Predict the values\n    .predict()\n```\n',
    'author': 'Mats E. Mollestad',
    'author_email': 'mats@mollestad.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/otovo/bender',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
