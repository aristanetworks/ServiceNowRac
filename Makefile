#!/usr/bin/make
# WARN: gmake syntax
########################################################
# Makefile for collector
#
# useful targets:
#	make check -- manifest checks
#	make clean -- clean up workspace
#	make pep8 -- pep8 checks
#	make pyflakes -- pyflakes checks
#	make pylint -- source code checks
#	make rpm -- build RPM package
#	make sdist -- build python source distribution
#	make systest -- runs the system tests
#	make tests -- run all of the tests
#
########################################################
# variable section

NAME = "ServiceNowRac"

PYTHON=python
COVERAGE=coverage
SITELIB = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

VERSION := $(shell awk '/__version__/{print $$NF}' ServiceNowRac/__init__.py | sed "s/'//g")

RPMSPECDIR = .
RPMSPEC = $(RPMSPECDIR)/ServiceNowRac.spec
RPMRELEASE = 1
RPMNVR = "$(NAME)-$(VERSION)-$(RPMRELEASE)"

PEP8_IGNORE = E302,E203,E261,E402
########################################################

all: clean check pep8 pyflakes pylint unittest coverage_report systest

check:
	check-manifest

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build rpmbuild
	rm -rf dist
	rm -rf MANIFEST
	rm -rf *.egg-info
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete

coverage_report:
	$(COVERAGE) report -m

pep8:
	-pep8 -r --ignore=$(PEP8_IGNORE) ServiceNowRac/ test/

pyflakes:
	pyflakes ServiceNowRac/ test/

pylint:
	find ./ServiceNowRac -name \*.py | xargs pylint --rcfile .pylintrc
	find ./test -name \*.py | xargs pylint --rcfile .pylintrc

unittest: clean
	$(COVERAGE) run --source $(NAME) -m unittest discover test/unit -v

systest: clean
	$(COVERAGE) run --source $(NAME) -m unittest discover test/system -v

tests: unittest systest

rpmcommon: sdist
	@mkdir -p rpmbuild
	@cp dist/*.gz rpmbuild/
	@sed -e 's#^Version:.*#Version: $(VERSION)#' -e 's#^Release:.*#Release: $(RPMRELEASE)#' $(RPMSPEC) >rpmbuild/$(NAME).spec

rpm: rpmcommon
	@rpmbuild --define "_topdir %(pwd)/rpmbuild" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	--define "_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
	--define "__python /usr/bin/python" \
	-ba rpmbuild/$(NAME).spec
	@rm -f rpmbuild/$(NAME).spec

sdist: clean
	$(PYTHON) setup.py sdist
