# Generate sphinx doc
docs:
	cd doc && ./autodoc_benchmarks.py > source/benchmarks.rst && make html

# Upload to PyPi
upload:
	python setup.py bdist sdist upload

# Install / uninstall using pip
install:
	pip install benchpress --user

uninstall:
	pip uninstall benchpress

# Install / Uninstall using setup.py
install_sp:
	python setup.py install --record=record.txt --user

uninstall_sp:
	@echo "Caution, 'rm -rf', the most dangerous command on earth, invoke it yourself."
	@echo "And check that record.txt contains what you want to remove."
	@echo "Or just remove those files in some other way."
	@echo 'rm -rf $$(cat record.txt)'

# Remove stuff...
clean:
	rm -f MANIFEST
	if [ -d "build" ]; then rm -rI build; fi
	if [ -d "dist" ]; then rm -rI dist; fi
	if [ -d "doc/build" ]; then rm -rI doc/build; fi
