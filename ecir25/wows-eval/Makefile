build-pypi-package: run-tests
	python3 -m build --sdist .
	python3 -m build --wheel .
	twine upload dist/wows_eval-0.0.2-py3-none-any.whl dist/wows_eval-0.0.2tar.gz

run-tests:
	pytest
