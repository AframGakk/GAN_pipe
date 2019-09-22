# Kubernetes setup



## Kubernetes and GCP

To get started with kubernetes and GCP see [here](https://cloud.google.com/kubernetes-engine/docs/quickstart).

### Pre-requires

1. make sure project is selected and API is enabled in [gcp kubernetes engine](https://console.cloud.google.com/projectselector/kubernetes?_ga=2.56338025.-392314001.1560242085)
2. Make sure billing is enabled
3. console requirements

### Requirements and installs

* gcloud
* kubectl
    ```bash
    gcloud components install kubectl
    ```
 
### Configurations

Setting a default project withing gcloud
````bash
gcloud config set project ml-project-1-247712
````

setting a default compute zone
```bash
gcloud config set compute/zone europe-west3-a
```

### Containerize app with cloud build

Setup Docker container for the service

Get the GCP project ID currently working on from terminal.

```bash
gcloud config get-value project
```

Build your container image using Cloud Build, which is similar to running docker build and docker push, but it happens on Google Cloud Platform (GCP). Replace PROJECT_ID with your GCP ID:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/test-app-1 ./
```

```bash
gcloud builds submit --tag gcr.io/ml-project-1-247712/test-app-1 ./
```
 
```bash
gcloud builds submit --tag gcr.io/ml-project-1-247712/test-app-2 ./
```

```bash
gcloud builds submit --tag gcr.io/ml-project-1-247712/test-app-3 ./
```

### Create kubernetes cluster

A GKE cluster is a managed set of Compute Engine virtual machines that operate as a single GKE cluster. This tutorial uses a single node.

Creating a cluster in a europe zone

```bash
gcloud container clusters create ai-offline-pipe \
   --num-nodes 3 \
   --enable-basic-auth \
   --issue-client-certificate \
   --zone europe-west3-a
```

OR for staging

```bash
gcloud container clusters create encode-ai-staging \
   --num-nodes 3 \
   --enable-basic-auth \
   --issue-client-certificate \
   --zone europe-west3-a
```

get the credentials so we can manage it locally through kubectl

```bash
gcloud container clusters get-credentials wisebeat \
    --zone europe-west2-a 
```


To verify that you have access to the cluster, this command lists the nodes in the cluster.

```bash
kubectl get nodes
```

### Deploy to GKE

Create a deployment yaml file in the source directory as deployment.yaml 

```yaml
# This file configures the hello-world app which serves public web traffic.
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: ai-offline-pipe
spec:
  replicas: 1
  selector:
    matchLabels:
      app: offline-pipe
  template:
    metadata:
      labels:
        app: offline-pipe
    spec:
      containers:
      - name: test-app-1
        # Replace [PROJECT_ID] with your project ID
        image: gcr.io/ml-project-1-247712/test-app-1:latest
        # This app listens on port 8080 for web traffic by default.
        ports:
        - containerPort: 8080
        env:
          - name: PORT
            value: "8080"
```

Deploy the resources to the cluster

```bash
kubectl apply -f deployment.yaml
```

You can track the status of the deployment with

```bash
kubectl get deployments
```

When deployment is complete, you can view the pods with.

```bash
kubectl get pods
```

### Deploy Service

Services provide a single point of access to a set of pods. While it's possible to access a single pod, pods are ephemeral 
and can only be accessed reliably by using a Service address. In your Hello World app, the "hello" Service defines a 
load balancer to access the hello-app pods from a single IP address. This Service is defined in the service.yaml file.

Create a service.yaml in same source directory

```yaml
# The hello service provides a load-balancing proxy over the hello-app
# pods. By specifying the type as a 'LoadBalancer', Kubernetes Engine will
# create an external HTTP load balancer.
apiVersion: v1
kind: Service
metadata:
  name: test-app-1
spec:
  type: LoadBalancer
  selector:
    app: test-app-1
  ports:
  - port: 80
    targetPort: 8080
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-app-1
spec:
  type: LoadBalancer
  selector:
    app: test-app-1
  ports:
  - port: 80
    targetPort: 8080
```

Create the service

```bash
kubectl apply -f service.yaml
```

Get the service external IP
```bash
kubectl get services
```

You have now deployed all the resources needed to run the Hello World app on GKE. Use the external IP address 
from the previous step to load the app in your web browser, and see your running app!
```bash
kubectl get service app-service \
    -o=custom-columns=NAME:.status.loadBalancer.ingress[*].ip --no-headers
curl 35.111.111.11
```

### Restart Pod
One way to restart a deployment of a pod is to scale it to zero and then back to original

```bash
kubectl scale deployment [POD_NAME] --replicas=0
kubectl scale deployment [POD_NAME] --replicas=1
```

```bash
kubectl scale deployment training-scheduler-deployment --replicas=0
kubectl scale deployment training-scheduler-deployment --replicas=1
```

### Describe Pod
Get what is going on with pod deployment

```bash
kubectl describe pod [POD_NAME]
```

```bash
kubectl describe pod training-scheduler-deployment
```

### Pod logging

In case the pod is crashing or is unhealthy we can use the following to view logs about whats happening.

```bash
kubectl logs [POD_NAME]
```

```bash
kubectl logs training-scheduler-deployment
```

the previous containers log

```bash
kubectl logs --previous [POD_NAME]
```

### Clean Up

To delete a cluster using the gcloud command-line tool, run the following command:
```bash
gcloud container clusters delete encode-ai-staging
```

To delete an image from one of your Container Registry repositories, run the following command:
```bash
gcloud container images delete gcr.io/ml-project-1-247712/test-app-1
gcloud container images delete gcr.io/ml-project-1-247712/test-app-2
gcloud container images delete gcr.io/ml-project-1-247712/test-app-3
```

Delete pod
```bash
kubectl delete pod [POD_NAME]
```

### Nodes

Resize the amount of nodes in the cluster
```bash
gcloud container clusters resize [CLUSTER_NAME] --num-nodes [NUM_NODES]
```


### Pods

ssh into a pod
````bash
kubectl exec -it [POD_NAME] -- /bin/bash
````

Get all pods detailed view
```bash
kubectl get pod -o wide
```




