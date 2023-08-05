# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_experiments']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.28,<2.0.0', 'pytest>=6.2.5,<7.0.0']

entry_points = \
{'pytest11': ['experiments = pytest_experiments.fixtures']}

setup_kwargs = {
    'name': 'pytest-experiments',
    'version': '0.1.0',
    'description': 'A pytest plugin to help developers of research-oriented software projects keep track of the results of their numerical experiments.',
    'long_description': '==================\npytest-experiments\n==================\n\n.. image:: https://img.shields.io/pypi/v/pytest-experiments.svg\n    :target: https://pypi.org/project/pytest-experiments\n    :alt: PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/pytest-experiments.svg\n    :target: https://pypi.org/project/pytest-experiments\n    :alt: Python versions\n\n.. image:: https://app.travis-ci.com/mbattifarano/pytest-experiments.svg?branch=main\n    :target: https://app.travis-ci.com/mbattifarano/pytest-experiments \n    :alt: See Build Status on travis\n\nA pytest plugin to help developers of research-oriented software projects keep track of the results of their numerical experiments.\n\n----\n\n\nWhat it does\n------------\n\n``pytest-experiments`` allows **research-oriented programmers** to easily\npersist data about **numerical experiments** so that they can **track\nmetrics over time**.\n\n1. Know **what** experiments you\'ve run, **when** you ran them, its\n   **inputs** and its **results** over time and project development.\n2. **Review and compare** experiments over time to ensure that\n   continued development is improving your results.\n\n\nHow it works\n------------\n\nAn **experiment** is a python function that runs your method or algorithm\nagainst some input and reports one or more metrics of interest. \n\nExperiments are basically `unit tests`_ of numerical methods. Like unit tests\nwe provide a function or method under test with some input and assert that its \noutput conforms to some concrete expectations. Unlike unit tests, the method \nunder test produces some metrics which we are interested in but for which\nconcrete expectations do not exist. We store these metrics, along with some\nmetadata in a database so that we can track our results over time.\n\nWe use ``pytest`` to collect and execute our experiments. This plugin offers\na ``notebook`` `fixture`_ to facilitate recording your experiments. Here is \na very simple example experiment:\n\n.. code-block:: python\n    \n    import pytest\n    from my_numerical_method_package import (\n        my_implementation,  # your numerical method\n        result_is_valid,    # returns True iff the result is well-formed\n        performance_metric, # the performance metric we care about\n    )\n\n    @pytest.mark.experiment  # [optional] mark this test as an experiment\n    @pytest.mark.parameterize("x", [1, 2, 3])  # The inputs; we will run this experiment for x=1, x=2, and x=3\n    def test_my_numerical_method(notebook, x):  # Request the notebook fixture\n        result = my_implementation(x)\n        assert result_is_valid(result)  # our concrete expectations about the result\n        notebook.record(performance=performance_metric(result))  # record the performance\n\nAt the end of the test the notebook fixture will save experiment metadata, the\ninputs, and whatever was passed to ``notebook.record`` to a database. By default,\nthis database will be a sqlite database called ``experiments.db``.\n\nA machine learning example\n^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nFor example, suppose we are building a machine learning classifier. The method\nunder test would be our model, the input would be train and validation\ndatasets and any hyper-parameters of our methods. The model is initialized \nwith the hyper-parameters, trained on the training data, and the output is the\npredictions on the validation set. \n\nWe want the model to return probabilities, so we have a concrete expectation\nthat the predictions should all be between 0 and 1. If any are not, our code \nis wrong and the experiment should fail.\n\nHowever, we are not only interested in returning probabilities, we also want\nour model to return good predictions (e.g. the predictions have high accuracy\nand high fairness). We might have some conrete expectations about these metrics:\nfor example we may wish to reject any result that has metrics strictly worse\nthan some baseline, but it is not easy or meaningful to specify a criterion\nbased on the accuracy and fairness values for when we should stop developing\nour model. In fact, the metrics collected during the experiment may inform\nsubsequent development.\n\nSee the ``demo`` directory for a detailed example-based walkthrough.\n\n\nInstallation\n------------\n\nYou can install "pytest-experiments" via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-experiments\n\n\nContributing\n------------\n\nContributions are very welcome. This project uses `poetry`_ for packaging.\n\nTo get set up simply clone the repo and run\n\n::\n\n    poetry install\n    poetry run pre-commit install\n\nThe first command will install the package along with all development dependencies\nin a virtual environment. The second command will install the pre-commit hook which\nwill automatically format source files with `black`_.\n\n\nTests can be run with ``pytest``\n\nPlease document any code added with docstrings. New modules can be auto-documented by \nrunning::\n\n    sphinx-apidoc -e -o docs/source src/pytest_experiments\n\nDocumentation can be compiled (for example to html with ``make``)::\n\n    cd docs/\n    make html\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-experiments" is free and open source software\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n\nAcknowledgements\n----------------\n\nThis `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_\'s `cookiecutter-pytest-plugin`_ template.\n\n\n.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter\n.. _`@hackebrot`: https://github.com/hackebrot\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause\n.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt\n.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0\n.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin\n.. _`file an issue`: https://github.com/mbattifarano/pytest-experiments/issues\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`pip`: https://pypi.org/project/pip/\n.. _`PyPI`: https://pypi.org/project\n.. _`black`: https://black.readthedocs.io/en/stable/\n.. _`unit tests`: https://en.wikipedia.org/wiki/Unit_testing\n.. _`fixture`: https://docs.pytest.org/en/latest/explanation/fixtures.html\n.. _`poetry`: https://python-poetry.org/',
    'author': 'Matt Battifarano',
    'author_email': 'matthew.battifarano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mbattifarano/pytest-experiments',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
