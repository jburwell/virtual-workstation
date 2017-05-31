PYTHON=python2

.PHONY: check
check: test

.PHONY: test
test:
	$(PYTHON) -m unittest discover
