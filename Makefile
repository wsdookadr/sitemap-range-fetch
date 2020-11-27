package_upload:
	rm -rf dist/ build/ sitemap_range_fetch.egg-info/
	python3 setup.py sdist bdist_wheel
	twine upload dist/*



