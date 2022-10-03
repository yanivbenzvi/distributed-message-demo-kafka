# Distributed system demo with Kafka over Kubernetes
This is a demo of a distributed system using Kafka over Kubernetes. It is based on the [Kafka quickstart](https://kafka.apache.org/quickstart) and [Kubernetes quickstart](https://kubernetes.io/docs/tutorials/stateless-application/hello-minikube/).

## Project description
In this project use the following dependencies:
- [FastAPI](https://fastapi.tiangolo.com/) as a web framework
- [aiokafka](https://aiokafka.readthedocs.io/en/stable/index.html) Asynchronous Kafka client to produce and consume messages in a synchronous way

## Prerequisites
* [Rancher Desktop](https://rancherdesktop.io/)
* [helm](https://helm.sh/docs/intro/install/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [python 3.10](https://www.python.org/downloads/)
* [poetry](https://python-poetry.org/docs/#installation)

## Setup
1. Start Rancher Desktop
2. Start a Kubernetes cluster
3. Install the Kafka helm chart
    ```bash
    make setup-infra
    ```
4. Build Producer and Consumer images
    ```bash
    make consumer-build
    make producer-build
    ```
5. Deploy Producer and Consumer
    ```bash
    make consumer-deploy
    make producer-deploy
    ```

## Usage
1. get the producer LoadBalancer IP and PORT
    ```bash
    export HOST=$(kubectl get service message-producer  --namespace message-system -o json | jq .spec.clusterIP | tr -d '"')
    export PORT=$(kubectl get service message-producer  --namespace message-system -o json | jq .spec.ports | jq '.[0]'.nodePort)
    ```
2. send a message to the producer
    ```bash
    curl --location --request GET "http://$HOST:$PORT/produce"
    ```
3. Now you can see the message in the consumer logs
    ```bash
    kubectl logs -f message-consumer-0 -n message-system
    ```