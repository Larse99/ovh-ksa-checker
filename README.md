
# KS-A Availability checker

KS-A is one of the best offerings from the OVH cloud, but the availability....
This application checks the availability of the KS-A server and sends a PushOver if there is any stock available :)

## Deployment
The preferred way of deploying this "application", is using Docker. It's also the easiest, since you don't need to install all the requirements or set up a Virtual Env.

### Docker
Using docker takes a couple of steps.

#### Building the container
Clone the repository and build the docker container

```bash
cd  KS-A_checker
docker  build  -t  ksa_checker  .
```

#### Deploying the container
It's possible to deploy it using a docker run command, but using a docker-compose file is easier. Isn't it? :)
```yaml
---
services:
  ksa-checker:
    image:  ovhscraper
    container_name:  ksa-checker
    env_file:  "docker.env"
    restart:  unless-stopped
```

#### Creating the env
The compose looks for a 'docker.env', where you define your environment variables. You can call it any way you want, aslong Docker can read it.

**PushOver Token**
PO_TOKEN=

**PushOver User Key**
PO_USER_KEY=

**OVH App Key**
OVH_APP_KEY=

**OVH App Secret**
OVH_APP_SECRET=

**OVH Consumer Key**
OVH_CONSUMER_KEY=

**Check interval - the amount of seconds the application should check. Default this is 60s, but can up to 1.**
CHECK_INTERVAL=

Setting the API keys is mandatory, the interval isn't.

## Issues
if you encounter any issues, let me know by creating a issue :-)
