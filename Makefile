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
	python -m pytest -vv tests/test_gantry.py

test_physical:
	python tests/physical_test.py

format:
	black *.py

run:
	#mosquitto & \
	python examples/main.py

run_server: install
	python autolab/server/server.py

all: install test format run_server