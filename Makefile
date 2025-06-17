.PHONY: all setup train extract membership adv plots report clean docker-build docker-run

setup:
	pip install --upgrade pip
	pip install -r requirements.txt

train:
	python src/model_train.py

extract:
	python src/extraction_attack.py

membership:
	python src/membership_attack.py

adv:
	python src/adversarial_tabular_attack.py

all: train extract membership adv

clean:
	rm -rf results/*.png results/report.html data/processed_data.pkl data/credit_model.pkl data/surrogate_model.pkl

docker-build:
	docker build -t poc-banking-ml-attacks .

docker-run:
	docker run --rm poc-banking-ml-attacks