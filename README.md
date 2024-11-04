# Collection of RabbitMQ Messaging Examples

This repository is a collection of implementations of RabbitMQ messaging using:
* [Direct Exchange](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchange-direct)
* [Fanout Exchange](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchange-fanout)
* [Topic Exchange](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchange-topic)
* [Remote Procedure Call (RPC)](https://www.rabbitmq.com/tutorials/tutorial-six-dotnet.html)
* [Default Exchange](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchange-default)

Build the container image for any one of the examples using the provided Dockerfile (build command for the RPC scenario below):

```
docker build -f Dockerfile --platform=linux/amd64 -t ashbourne1990/rabbitmq-rpc-example:latest remote-procedure-call
```

Deploy the RabbitMQ server locally by running:

```
docker run -d --hostname rabbitmq-local --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```

Deploy RabbitMQ on Kubernetes by running:

```
kubectl apply -f rabbitmq-server/deployment/rabbitmq-server.yml
```

The YML manifests for each messaging scenario (Direct Exchange, Fanout Exchange, etc.) are available under the ```producer``` and ```consumer``` folders

Create a Kubernetes Secret with default (or custom) RabbitMQ credentials (within every Namespace with workloads connecting to the cluster):

```
kubectl create secret generic -n application rmq-credentials --from-literal=username=guest --from-literal=password=guest
```
