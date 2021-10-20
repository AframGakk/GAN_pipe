# Wisebeat GAN engine

The wisebeat engine is a specially designed stream engine pipeline for training generative adverserial networks in sound processing.
The data lakes are located at GCP storage.

## Local Dev setup

The entire engine is written in python 3.7 with docker deployment to local environment for testing and GCP kubernetes
deployment to staging and production.

### Requirements

* Python 3.7
* pip
* gcloud
* docker
* GCP dev credential file (contact system admin)
* Jenkins server credentials (contact admin)


### Additional requirements for OSX
* homebrew
 
#### OSX homebrew install
Follow the [Official homebrew](https://brew.sh/) install instructions. (Once terminal command)
 
#### Python install linux

To check if installed
````bash
python --version
````

Update apt-get
```bash
sudo apt-get update
```

```bash
sudo apt-get install python
```

confirm install
```bash
python --version
```

#### Python install OSX
Make sure homebrew has been installed

install with homebrew
```bash
brew install python
```

verify install
```bash
python --version
```

#### Pip install linux

To check if installed
````bash
pip --version
````

Update apt-get
```bash
sudo apt-get update
```

```bash
sudo apt-get install pip
```

confirm install
```bash
pip --version
```
#### pip install OSX
Make sure homebrew has been installed

install with homebrew
```bash
brew install pip
```

verify install
```bash
pip --version
```

### System setup

The system is built in a microserviced manner and therefore each service should be ran 
indivitually both in production and in development. To set up a service make sure you 
are using a terminal and are located at the root level at each service (./ControllerService, ./GAN).

Install virtual environment.

```bash
pip install virtualenv
```

Create virtual environment

```bash
virtualenv venv
```

Activate the environment

```bash
source venv/bin/activate
```

Install all requirements for the service.

```bash
pip install -r requirements.txt
```

Running each "Controller" starts the broker service for each component.






