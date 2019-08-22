# Jenkins Setup

## Install (Ubuntu)

### Install

Install Java and update apt
```bash
sudo apt update
sudo apt install openjdk-8-jdk
```

Add the jenkins debian repository
```bash
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
```

Add jenkins repository to the system
```bash
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
```

Install Jenkins
```bash
sudo apt update
sudo apt install jenkins
```

When you install Jenkins the service automatically starts and you can check it here
```bash
systemctl status jenkins
```

### Firewall setup

Jenkins runs on port 8080 and therefore we need to open up for port 8080 on firewall if the firewall is active.
```bash
sudo ufw allow 8080
```

To verify
```bash
sudo ufw status
```

### Setup

instance dependancies
* git
* python 3.7
* docker
* gcloud
* kubectl via gcloud
* 





