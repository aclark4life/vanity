pre:
	virtualenv .
	bin/pip install -r requirements.txt
	check-manifest
	pyroma .
	viewdoc
