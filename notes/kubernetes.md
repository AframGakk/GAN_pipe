## Kubernetes

Get all nodes 
```bash
kubectl get nodes
```

### Running local kubernetes

You are finally ready to get the application running in Kubernetes. Because you have a web application, you will 
create a service and a deployment. First verify your kubectl is configured. At the command line, type the following:

```bash
kubectl version
```

If you don’t see a reply with a Client and Server version, you’ll need to install and configure it.
If you are running on Windows or Mac, make sure it is using the Docker for Desktop context by running the following:

```bash
kubectl config use-context docker-for-desktop
```

```bash
kubectl get nodes
```



