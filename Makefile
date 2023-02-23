build:
	git pull
	pip3 install -r requirements.txt
	rm -rf dist/
	pyinstaller --onefile main.py
	rm *.spec
