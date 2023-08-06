test:
	python2 -m unittest preserves.test_preserves
	python3 -m unittest preserves.test_preserves

coverage:
	python2-coverage run --branch -m unittest preserves.test_preserves
	python3-coverage run --branch -m unittest preserves.test_preserves
	python3-coverage html

clean:
	rm -rf htmlcov
	find . -iname __pycache__ -o -iname '*.pyc' | xargs rm -rf
	rm -f .coverage
	rm -rf preserves.egg-info build dist

publish: clean build
	# sudo apt install python3-wheel twine
	twine upload dist/*

build:
	python3 setup.py sdist bdist_wheel
