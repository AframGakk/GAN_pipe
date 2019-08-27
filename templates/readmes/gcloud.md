# gcloud instructions


## Installs

### gcloud
* [ubuntu linux](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu)
* [windows](https://cloud.google.com/sdk/docs/quickstart-windows)  
* [mac](https://cloud.google.com/sdk/docs/quickstart-macos)


### User and IAM configs

Active user configured
```BASH
gcloud config list account --format "value(core.account)"
```

View autenticated user list
```bash
gcloud auth list
```

To set a specific account (replace "ACCOUNT" with the account to switch)
```bash
gcloud config set account "ACCOUNT"
```
  
#### Service accounts

Create service account
```bash
gcloud iam service-accounts create [ACCOUNT_NAME]
```

List all service-accounts
```bash
gcloud iam service-accounts list
```

Download service account key
```bash
gcloud iam service-accounts keys create api.json --iam-account [SERVICE_ACCOUNT_EMAIL]
```

Activate a service account. Replace [THE_CRED_FILE] with the location of the json credential file
```bash
gcloud auth activate-service-account --key-file=[THE_CRED_FILE]
```



### Project config

Check what project you are currently signed on
```bash
.gcp > gcloud config list --format 'value(core.project)' 2>/dev/null
```

List all projects authenticated user has access to
```bash
gcloud projects list
```

Change to a specific project
```bash
gcloud config set project [PROJECT_ID]
```

### Buckets

List all buckets in project
```bash
gsutil ls
```

### Compute Instances

List all compute instances
```bash
gcloud compute instances list
```

ssh to an instance
```bash
gcloud compute ssh [INSTANCE_NAME]
```



