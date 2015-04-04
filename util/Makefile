#
# This Makefile is intended for aiding development of Benchpress,
# it is not an interface for using Benchpress.
#
# Using this Makefile assumes that you are running from clone.
# Remember to set PATH and PYTHONPATH before using this Makefile:
#
# cd ../ && source util/setbpenv.bash
#
DOCSRC := $(shell bp-info --docsrc)
MOD_PARENT := $(shell bp-info --mod_parent)

# Install / uninstall using pip
install:
	pip install benchpress --user

uninstall:
	pip uninstall benchpress

# Generate sphinx doc
docs:
	cd $(DOCSRC) && ./autodoc_benchmarks.py > source/benchmarks.rst
	cd $(DOCSRC) && bp-info -h > source/usage_bp-info.out
	cd $(DOCSRC) && bp-run -h > source/usage_bp-run.out
	cd $(DOCSRC) && bp-times -h > source/usage_bp-times.out
	cd $(DOCSRC) && bp-grapher -h > source/usage_bp-grapher.out
	cd $(DOCSRC) && bp-compile -h > source/usage_bp-compile.out
	cd $(DOCSRC) && make html

# Upload to PyPi
upload:
	cd $(MOD_PARENT) && python setup.py bdist sdist upload

# Install / Uninstall using setup.py
install_sp:
	cd $(MOD_PARENT) && python setup.py install --record=record.txt --user

uninstall_sp:
	@echo "Caution, 'rm -rf', the most dangerous command on earth, invoke it yourself."
	@echo "And check that record.txt contains what you want to remove."
	@echo "Or just remove those files in some other way."
	@echo 'rm -rf $$(cat $(MOD_PARENT)/record.txt)'

# Remove stuff...
clean:
	rm -f $(MOD_PARENT)/MANIFEST
	if [ -d "$(MOD_PARENT)/dist" ]; then rm -rI $(MOD_PARENT)/dist; fi
	if [ -d "$(DOCSRC)/build" ]; then rm -rI $(DOCSRC)/build; fi
