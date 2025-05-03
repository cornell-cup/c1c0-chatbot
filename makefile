CHATBOT_PATH := $(shell pwd)
PYTHON_VER   := 3.11

run:
	venv/bin/python chatbot.py

install:
	venv/bin/pip install -r requirements.txt
	venv/bin/python -m spacy download en_core_web_sm

venv:
	python$(PYTHON_VER) -m venv venv/
	venv/bin/pip install --upgrade pip setuptools wheel
