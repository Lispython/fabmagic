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
	cd examples/fabmagic_box && vagrant up && cd ../../

vms-stop:
	cd examples/fabmagic_box && vagrant halt && cd ../../

vms-destroy:
	cd examples/fabmagic_box && vagrant destroy && cd ../../

vms-prepare:
	cd /tmp
	wget http://files.vagrantup.com/lucid32.box
	wget http://files.vagrantup.com/precise32.box
	vagrant add fabmagic_box_lucid32 /tmp/lucid32.box
	vagrant add fabmagic_box_precise32 /tmp/precise32.box