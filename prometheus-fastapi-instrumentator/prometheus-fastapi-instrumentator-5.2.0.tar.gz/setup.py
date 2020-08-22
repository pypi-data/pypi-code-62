# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prometheus_fastapi_instrumentator']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.38.1,<=1.0.0', 'prometheus-client>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'prometheus-fastapi-instrumentator',
    'version': '5.2.0',
    'description': 'Instrument your FastAPI with Prometheus metrics',
    'long_description': '# Prometheus FastAPI Instrumentator\n\n[![PyPI version](https://badge.fury.io/py/prometheus-fastapi-instrumentator.svg)](https://pypi.python.org/pypi/prometheus-fastapi-instrumentator/)\n[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n[![downloads](https://pepy.tech/badge/prometheus-fastapi-instrumentator/month)](https://pepy.tech/project/prometheus-fastapi-instrumentator/month)\n[![docs](https://img.shields.io/badge/docs-here-blue)](https://trallnag.github.io/prometheus-fastapi-instrumentator/)\n\n![release](https://github.com/trallnag/prometheus-fastapi-instrumentator/workflows/release/badge.svg)\n![test branches](https://github.com/trallnag/prometheus-fastapi-instrumentator/workflows/test%20branches/badge.svg)\n[![codecov](https://codecov.io/gh/trallnag/prometheus-fastapi-instrumentator/branch/master/graph/badge.svg)](https://codecov.io/gh/trallnag/prometheus-fastapi-instrumentator)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA configurable and modular Prometheus Instrumentator for your FastAPI. Install \n`prometheus-fastapi-instrumentator` from \n[PyPI](https://pypi.python.org/pypi/prometheus-fastapi-instrumentator/). Here \nis the fast track to get started with a sensible preconfigured instrumentator:\n\n```python\nfrom prometheus_fastapi_instrumentator import Instrumentator\n\nInstrumentator().instrument(app).expose(app)\n```\n\nWith this, your FastAPI is instrumented and metrics ready to be scraped. The \nsensible defaults give you:\n\n* Counter `http_requests_total` with `handler`, `status` and `method`. Total \n    number of requests.\n* Summary `http_request_size_bytes` with `handler`. Added up total of the \n    content lengths of all incoming requests. If the request has no valid \n    content length header it will be ignored. No percentile calculated.\n* Summary `http_response_size_bytes` with `handler`. Added up total of the \n    content lengths of all outgoing responses. If the response has no valid \n    content length header it will be ignored. No percentile calculated.\n* Histogram `http_request_duration_seconds` with `handler`. Only a few buckets \n    to keep cardinality low. Uses for aggregations by handler or SLI buckets.\n* Histogram `http_request_duration_highr_seconds` without any labels. Large \n    number of buckets (>20) for accurate percentile calculations.\n\nIn addition, following behaviour is active:\n\n* Status codes are grouped into `2xx`, `3xx` and so on.\n* Requests without a matching template are grouped into the handler `none`.\n\nIf one of these presets does not suit your needs you can simply tweak \nthe instrumentator with one of the many parameters or roll your own metrics.\n\n---\n\nContents: **[Features](#features)** |\n**[Advanced Usage](#advanced-usage)** | \n[Creating the Instrumentator](#creating-the-instrumentator) |\n[Adding metrics](#adding-metrics) |\n[Creating new metrics](#creating-new-metrics) |\n[Perform instrumentation](#perform-instrumentation) |\n[Exposing endpoint](#exposing-endpoint) |\n**[Documentation](#documentation)** |\n**[Prerequesites](#prerequesites)** |\n**[Development](#development)**\n\n---\n\n## Features\n\nBeyond the fast track, this instrumentator is **highly configurable** and it \nis very easy to customize and adapt to your specific use case. Here is \na list of some of these options you may opt-in to:\n\n* Regex patterns to ignore certain routes.\n* Completely ignore untemplated routes.\n* Control instrumentation and exposition with an env var.\n* Rounding of latencies to a certain decimal number.\n* Renaming of labels and the metric.\n\nIt also features a **modular approach to metrics** that should instrument all \nFastAPI endpoints. You can either choose from a set of already existing metrics \nor create your own. And every metric function by itself can be configured as \nwell. You can see ready to use metrics [here](https://trallnag.github.io/prometheus-fastapi-instrumentator/metrics.html).\n\n## Advanced Usage\n\nThis chapter contains an example on the advanced usage of the Prometheus \nFastAPI Instrumentator to showcase most of it\'s features. Fore more concrete \ninfo check out the \n[automatically generated documentation](https://trallnag.github.io/prometheus-fastapi-instrumentator/).\n\n### Creating the Instrumentator\n\nWe start by creating an instance of the Instrumentator. Notice the additional \n`metrics` import. This will come in handy later.\n\n```python\nfrom prometheus_fastapi_instrumentator import Instrumentator, metrics\n\ninstrumentator = Instrumentator(\n    should_group_status_codes=False,\n    should_ignore_untemplated=True,\n    should_respect_env_var=True,\n    excluded_handlers=[".*admin.*", "/metrics"],\n    env_var_name="ENABLE_METRICS",\n)\n```\n\nUnlike in the fast track example, now the instrumentation and exposition will \nonly take place if the environment variable `ENABLE_METRICS` is `true` at \nrun-time. This can be helpful in larger deployments with multiple services\ndepending on the same base FastAPI.\n\n### Adding metrics\n\nLet\'s say we also want to instrument the size of requests and responses. For \nthis we use the `add()` method. This method does nothing more than taking a\nfunction and adding it to a list. Then during run-time every time FastAPI \nhandles a request all functions in this list will be called while giving them \na single argument that stores useful information like the request and \nresponse objects. If no `add()` at all is used, the default metric gets added \nin the background. This is what happens in the fast track example.\n\nAll instrumentation functions are stored as closures in the `metrics` module. \nClosures come in handy here because it allows us to configure the functions \nwithin.\n\n```python\ninstrumentator.add(metrics.latency(buckets=(1, 2, 3,)))\n```\n\nThis simply adds the metric you also get in the fast track example with a \nmodified buckets argument. But we would also like to record the size of \nall requests and responses. \n\n```python\ninstrumentator.add(\n    metrics.request_size(\n        should_include_handler=True,\n        should_include_method=False,\n        should_include_status=True,\n        metric_namespace="a",\n        metric_subsystem="b",\n    )\n).add(\n    metrics.response_size(\n        should_include_handler=True,\n        should_include_method=False,\n        should_include_status=True,\n        metric_namespace="namespace",\n        metric_subsystem="subsystem",\n    )\n)\n```\n\nYou can add as many metrics you like to the instrumentator.\n\n### Creating new metrics\n\nAs already mentioned, it is possible to create custom functions to pass on to\n`add()`. Let\'s say we want to count the number of times a certain language \nhas been requested.\n\n```python\ndef http_requested_languages_total() -> Callable[[Info], None]:\n    METRIC = Counter(\n        "http_requested_languages_total", \n        "Number of times a certain language has been requested.", \n        labelnames=("langs",)\n    )\n\n    def instrumentation(info: Info) -> None:\n        langs = set()\n        lang_str = info.request.headers["Accept-Language"]\n        for element in lang_str.split(",")\n            element = element.split(";")[0].strip().lower()\n            langs.add(element)\n        for language in langs:\n            METRIC.labels(language).inc()\n\n    return instrumentation\n```\n\nThe function `http_requested_languages_total` is used for persistent elements \nthat are stored between all instrumentation executions (for example the \nmetric instance itself). Next comes the closure. This function must adhere \nto the shown interface. It will always get an `Info` object that contains \nthe request, response and a few other modified informations. For example the \n(grouped) status code or the handler. Finally, the closure is returned.\n\nTo use it, we hand over the closure to the instrumentator object.\n\n```python\ninstrumentator.add(http_requested_languages_total())\n```\n\n### Perform instrumentation\n\nUp to this point, the FastAPI has not been touched at all. Everything has been \nstored in the `instrumentator` only. To actually register the instrumentation \nwith FastAPI, the `instrument()` method has to be called.\n\n```python\ninstrumentator.instrument(app)\n```\n\nNotice that this will do nothing if `should_respect_env_var` has been set \nduring construction of the instrumentator object and the respective env var \nis not found.\n\n### Exposing endpoint\n\nTo expose an endpoint for the metrics either follow \n[Prometheus Python Client](https://github.com/prometheus/client_python) and \nadd the endpoint manually to the FastAPI or serve it on a separate server.\nYou can also use the included `expose` method. It will add an endpoint to the \ngiven FastAPI.\n\n```python\ninstrumentator.expose(app, include_in_schema=False)\n```\n\nNotice that this will to nothing if `should_respect_env_var` has been set \nduring construction of the instrumentator object and the respective env var \nis not found.\n\n## Documentation\n\nThe documentation is hosted [here](https://trallnag.github.io/prometheus-fastapi-instrumentator/).\n\n## Prerequesites\n\n* `python = "^3.6"` (tested with 3.6 and 3.8)\n* `fastapi = ">=0.38.1, <=1.0.0"` (tested with 0.38.1 and 0.61.0)\n* `prometheus-client = "^0.8.0"` (tested with 0.8.0)\n\n## Development\n\nDeveloping and building this package on a local machine requires \n[Python Poetry](https://python-poetry.org/). I recommend to run Poetry in \ntandem with [Pyenv](https://github.com/pyenv/pyenv). Once the repository is \ncloned, run `poetry install` and `poetry shell`. From here you may start the \nIDE of your choice.\n\nTake a look at the Makefile or workflows on how to test this package.\n',
    'author': 'Tim Schwenke',
    'author_email': 'tim.schwenke+trallnag@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trallnag/prometheus-fastapi-instrumentator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
