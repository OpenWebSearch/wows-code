build-pypi-package: run-tests
	rm -Rf dist
	python3 -m build --sdist .
	python3 -m build --wheel .
	twine upload dist/wows_eval-*-py3-none-any.whl dist/wows_eval-*.tar.gz

run-tests:
	pytest
