producer-build:
	docker build -t localhost:5000/producer:1.5 -f producer/Dockerfile producer

producer-deploy:
	helm upgrade -i message-producer infra/producer --namespace message-system --create-namespace --values infra/producer/values.yaml

producer-uninstall-helm:
	helm uninstall message-producer --namespace message-system

consumer-build:
	docker build -t localhost:5000/consumer:1.5 -f consumer/Dockerfile consumer

consumer-deploy:
	helm upgrade -i message-consumer infra/consumer --namespace message-system --create-namespace --values infra/consumer/values.yaml

consumer-uninstall-helm:
	helm uninstall message-consumer --namespace message-system


setup-infra:
	@echo "Running infra"

	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add kafka-ui https://provectus.github.io/kafka-ui

	helm dependency build infra/message-system
	helm upgrade -i message-service infra/message-system --namespace message-system --create-namespace --values=infra/message-system/values.yaml

	@echo "Waiting for kafka to be ready"
	sleep 10

	@echo "Forwarding Kafka UI port"
	kubectl port-forward -n message-system svc/message-service-kafka-ui 8080:80
	#kubectl port-forward -n message-system svc/message-service-kafka-cluster 9092:9092

	# TODO: add a check for kafka is ready:
	# @echo "Waiting for kafka to be ready"
	# @while [ $(kubectl get pods -n message-system -l app.kubernetes.io/name=kafka -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]; do echo "waiting for kafka" && sleep 1; done
	# @echo "Kafka is ready"

	#helm upgrade --install message-service infra/message-service --create-namespace --namespace distributed-system

uninstall-infra:
	helm delete message-service --namespace message-system