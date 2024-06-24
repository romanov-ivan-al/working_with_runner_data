all: clean build

build:
	python3 main.py

clean:
	rm -rf __pycache__ test.txt  m15.json m16.json m18.json w15.json w16.json w18.json