all: clean-pyc test

test:
	python setup.py nosetests --stop --tests tests.py

travis:
	python setup.py nosetests --tests tests.py

coverage:
	python setup.py nosetests  --with-coverage --cover-package=fabmagic --cover-html --cover-html-dir=coverage_out coverage


shell:
	../venv/bin/ipython

audit:
	python setup.py autdit

release:
	python setup.py sdist upload

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

find-print:
	grep -r --include=*.py --exclude-dir=venv --exclude=fabfile* --exclude=tests.py --exclude-dir=tests --exclude-dir=commands 'print' ./


vms-start:
	cd examples/fabmagic_box_lucid32 && vagrant up && cd ../../
	cd examples/fabmagic_box_precise32 && vagrant up && cd ../../

vms-stop:
	cd examples/fabmagic_box_lucid32 && vagrant halt && cd ../../
	cd examples/fabmagic_box_precise32 && vagrant halt && cd ../../