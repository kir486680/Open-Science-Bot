install:
	if grep -q Raspberry /proc/cpuinfo; then \
		pip install --upgrade pip &&\
		pip install -r requirements_raspi.txt; \
	else \
		pip install --upgrade pip &&\
		pip install -r requirements.txt; \
	fi
	#sudo apt-get install -y mosquitto
	#sudo apt-get install libgl1

test:
	python -m pytest -vv tests/testGantry.py

format:
	black *.py

lint:
	pylint --disable=R,C main.py

run:
	#mosquitto & \
	python main.py

all: install test format