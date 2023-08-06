all: test

test:
	python -m unittest discover -v

dep:
	python -m pip install -r requirements.txt

install: dep
	python -m pip install -e .

export:
	python -c 'from welib.tools.repo import *; export_figs_rec("welib/");'


clean:
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist



pypi0:
	python setup.py sdist bdist_wheel

pypi1:
	twine upload --repository testpypi dist/*

pypi2:
	twine upload dist/*


pipun:
	python -m pip freeze > _pip_temp && pip uninstall -y -r _pip_temp


example:
	python welib/beams/examples/Ex1_BeamModes.py
