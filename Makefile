test:
	virtualenv .
	bin/pip install -r requirements.txt
	check-manifest
	pyroma .
	flake8 *.py
	python setup.py test
	viewdoc
