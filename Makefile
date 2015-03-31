docs:
	cd doc && ./autodoc_benchmarks.py > source/benchmarks.rst && make html

upload:
	python setup.py bdist sdist upload

install:
	python setup.py install --record=record.txt --user

uninstall:
	@echo "Caution, 'rm -rf', the most dangerous command on earth, invoke it yourself."
	@echo "And check that record.txt contains what you want to remove."
	@echo "Or just remove those files in some other way."
	@echo 'rm -rf $$(cat record.txt)'

clean:
	git clean -fd
	if [ -d "build" ]; then rm -rI build; fi
	if [ -d "dist" ]; then rm -rI dist; fi
	if [ -d "doc/build" ]; then rm -rI doc/build; fi
