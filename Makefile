# https://github.com/aclark4life/python-project
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Alex Clark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Django
project = project
app = app

# Python
package = $(project)

all: up
branches=`git branch -a | grep remote | grep -v HEAD | grep -v master`
clean:
	find . -name \*.pyc | xargs rm -v
clean-migrations:
	rm -rf $(project)/$(app)/migrations
clean-postgres:
	-dropdb $(project)-$(app)
	-createdb $(project)-$(app)
clean-sqlite:
	-rm -f db.sqlite3
	-git add db.sqlite3
co:
	-for i in $(branches) ; do \
        git checkout -t $$i ; \
    done
commit:
	git commit -a
commit-update:
	git commit -a -m "Update"
db: migrate su
flake:
	-flake8 *.py
	-flake8 $(project)/*.py
	-flake8 $(project)/$(app)/*.py
# http://stackoverflow.com/a/26339924
.PHONY: help
help:
	@echo "\nPlease call with one of these targets:\n"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F:\
        '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}'\
        | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs | tr ' ' '\n' | awk\
        '{print "    - "$$0}'
	@echo "\n"
install:
	virtualenv .
	bin/pip install -r requirements.txt
lint: yapf flake wc
migrate:
	python manage.py migrate
migrations:
	python manage.py makemigrations $(app)
package-test:
	check-manifest
	pyroma .
push: push-origin
push-heroku:
	git push heroku
push-origin:
	git push
review:
	open -a "Sublime Text 2" `find $(project) -name \*.py | grep -v __init__.py`\
        `find $(project) -name \*.html`
serve:
	python manage.py runserver
shell:
	python manage.py shell
shell-heroku:
	heroku run bash
start:
	-mkdir -p $(project)/$(app)
	-django-admin startproject $(project) .
	-django-admin startapp $(app) $(project)/$(app)
su:
	python manage.py createsuperuser
test:
	python manage.py test
test-readme:
	rst2html.py README.rst > readme.html; open readme.html
update: commit
up: commit-update push
upload-test:
	python setup.py sdist --format=gztar,zip upload -r test
upload:
	python setup.py sdist --format=gztar,zip upload
wc:
	wc -l *.py
	wc -l $(project)/*.py
	wc -l $(project)/$(app)/*.py
yapf:
	-yapf -i *.py
	-yapf -i -e $(project)/urls.py $(project)/*.py
	-yapf -i $(project)/$(app)/*.py
