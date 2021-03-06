SHELL = /bin/bash

listen=localhost:8000
baseurl=http://$(listen)
root=$(shell pwd)
user=$(shell whoami)
version=$(shell git describe --tags --abbrev=0)
arch=$(shell uname -p)


etc/settings.ini:
	mkdir -p etc/
	cp conf/settings.ini.sample etc/settings.ini

bin/phantomjs:
	mkdir -p lib/
	wget http://phantomjs.googlecode.com/files/phantomjs-1.8.1-linux-$(arch).tar.bz2 -O phantomjs.tar.bz2
	rm -rf $(root)/lib/*phantomjs*/
	tar -jxvf phantomjs.tar.bz2 -C $(root)/lib/
	rm phantomjs.tar.bz2
	ln -sf $(root)/lib/*phantomjs*/bin/phantomjs $(root)/bin/
	# Install system-wide binary (require sudo)
	sudo ln -sf $(root)/bin/phantomjs /usr/local/bin/

bin/casperjs: bin/phantomjs
	wget https://github.com/n1k0/casperjs/zipball/1.0.1 -O casperjs.zip
	rm -rf $(root)/lib/*casperjs*/
	unzip -o casperjs.zip -d $(root)/lib/ > /dev/null
	rm casperjs.zip
	ln -sf $(root)/lib/*casperjs*/bin/casperjs $(root)/bin/
	# Install system-wide binary (require sudo)
	sudo ln -sf $(root)/bin/casperjs /usr/local/bin/

bin/python:
	virtualenv .
	mkdir -p lib/eggs
	wget http://python-distribute.org/bootstrap.py
	bin/python bootstrap.py --version=1.6.3
	rm bootstrap.py

install: etc/settings.ini bin/python bin/casperjs

clean_harmless:
	find geotrek/ -name "*.pyc" -exec rm -f {} \;
	rm -f install

clean: clean_harmless
	rm -rf bin/ lib/ local/ include/ *.egg-info/
	rm -rf var/
	rm -rf etc/init/
	rm -f .installed.cfg
	rm -f install.log

.PHONY: all_makemessages all_compilemessages

all_makemessages: install
	for dir in `find geotrek/ -type d -name locale`; do pushd `dirname $$dir` > /dev/null; $(root)/bin/django-admin makemessages -a; popd > /dev/null; done

all_compilemessages: install
	for dir in `find geotrek/ -type d -name locale`; do pushd `dirname $$dir` > /dev/null; $(root)/bin/django-admin compilemessages; popd > /dev/null; done

release:
	git archive --format=zip --prefix="geotrek-$(version)/" $(version) > ../geotrek-src-$(version).zip

unit_tests: install clean_harmless
	bin/buildout -Nvc buildout-tests.cfg
	bin/develop update -f
	bin/django jenkins --coverage-rcfile=.coveragerc --output-dir=var/reports/ authent core land maintenance trekking common infrastructure mapentity

unit_tests_js:
	casperjs --baseurl=$(baseurl) --reportdir=var/reports geotrek/tests/test_qunit.js

functional_tests:
	casperjs --baseurl=$(baseurl) --save=var/reports/FUNC-auth.xml geotrek/tests/auth.js
	casperjs --baseurl=$(baseurl) --save=var/reports/FUNC-88.xml geotrek/tests/story_88_user_creation.js
	casperjs --baseurl=$(baseurl) --save=var/reports/FUNC-test_utils.xml geotrek/tests/test_utils.js

tests: unit_tests functional_tests

serve: install clean_harmless all_compilemessages
	bin/buildout -Nvc buildout-dev.cfg
	bin/django syncdb --noinput --migrate
	bin/django runcserver $(listen)

load_data:
	# /!\ will delete existing data
	bin/django loaddata minimal
	bin/django loaddata basic
	for dir in `find geotrek/ -type d -name upload`; do pushd `dirname $$dir` > /dev/null; cp -R upload/* $(root)/var/media/upload/ ; popd > /dev/null; done

deploy: install clean_harmless
	bin/buildout -Nc buildout-prod.cfg buildout:user=$(user)
	sudo chgrp -R $(user) var/
	sudo chmod -R g+w var/
	touch lib/parts/django/django_extrasettings/settings_production.py
	make all_compilemessages
	bin/develop update -f
	bin/django syncdb --noinput --migrate
	bin/django collectstatic --clear --noinput --verbosity=0
	bin/django update_translation_fields
	bin/supervisorctl restart all

deploy_demo: deploy load_data
	bin/django loaddata development-pne
