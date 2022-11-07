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