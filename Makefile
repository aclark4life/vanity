test:
	virtualenv .
	bin/pip install -r requirements.txt
	check-manifest
	pyroma .
	-flake8 *.py
	python setup.py test
	viewdoc
upload-test:
	python setup.py sdist --format=gztar,zip upload -r test
upload:
	python setup.py sdist --format=gztar,zip upload
