# transport-infrastructure-etl


Notes to myself on setting up development environment, building the docker images amd executing on AWS EC2.

## Python development environment

My python script and pipfile developemnt environment is my local windows machine. Python scripts are exectuted from the Pwoershell command line. AWS CLI is needed for authenicating to AWS (IAM not available in the local dev envirionment) which is necessary for using the AWS Python SDK (boto3) and for working with AWS ECR. 

The specific versions of python pacake requirements can be locked using:

> pipenv lock

### Development environment requirements

1. Pipenv
2. AWS CLI 

## Docker Image development environment

The dockerfile is located in transport-infrastructure-etl/docker.

Build the latest dockerfile and python code and lauch a container locally using the docker-compose.yaml file located in the same location:

> cd docker
> docker-compose up --build -d

### Pushing the latest docker image to ECR 

Run the follwing command on the Powersheel command line:

First, you may need to authenticate with ECR if token has expired:

> aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 157782876633.dkr.ecr.eu-west-1.amazonaws.com

Tag the traffic_etl image with the AWS ECR name:

> docker tag traffic_etl:latest 157782876633.dkr.ecr.eu-west-1.amazonaws.com/traffic_etl:latest

Push the image to my ECR account:

> docker push 157782876633.dkr.ecr.eu-west-1.amazonaws.com/traffic_etl:latest

### Executing the docker image on EC2 

This section assumes you have an ubuntu EC2 instance available with Dokcer and t heAWS CLI installed.

SCP over docker/docker-compose-ec2.yaml to the EC2 instance.

SSH into the EC2 instance.

Run thefollwing commands:

> docker-compose pull etl 
> docker-compose up --build


