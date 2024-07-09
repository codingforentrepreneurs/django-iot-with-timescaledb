# Django IoT with TimescaleDB

Learn how to distribute Django across IoT Devices (Raspberry PI) to collect Time Series data from sensors using TimescaleDB.



## Getting Started with Ansible, Raspberry Pis, Django, and TimescaleDB

Ansible will help automate the configuration for however many Raspberry Pis you have.

Going forward, each Raspberry Pi will be configured with the root user as `cfe` and each Pi will have a unique hostname with the pattern:

- `djangopi`
- `djangopi-2`
- `djangopi-3`
- etc

To access these pis on your local network, you can use:

```bash
ssh cfe@djangopi.local
```

This configuration is done when you flash (aka install) the Raspberry Pi on a new MicroSD card with the [Raspberry Pi Imager](https://www.raspberrypi.com/software/). The OS used will be dependant on your Raspberry Pi version. For this guide, sed the headless os called _Raspberry Pi Lite (64-bit)_ with custom settings to automatically:

- set hostname (`djangopi`, etc)
- set root user (`cfe`)
- connect to my local wifi
- install my SSH public key (`~/.ssh/id_rsa.pub`) for passwordless SSH sessions (very useful for Ansible)

### 1. Clone this repo

```bash
mkdir -p django-iot
cd django-iot
git clone https://github.com/codingforentrepreneurs/django-iot-with-timescaledb .
```

### 2. Create virtual environment and install dev packages

_mac/linux/wsl_
```bash
python3 -m venv venv
source venv/bin/activate
```

_windows powershell_ 
```powershell
c:\path\to\python.exe -m venv venv
.\venv\Scripts\activate
```

With virtual environment activated:
```bash
pip install --upgrade pip
pip install -r requirements.dev.txt
pip install -r requirements.txt
```


### 3. Create `.env.prod` for encrypted environment variables

```bash
cp .env.web-sample .env.prod
```

Ensure `.env.prod` resembles:
```bash
DJANGO_SECRET_KEY="django-insecure-ajq-plfh&4uh6rea1zliteu+bszy57v*g%t0t^j2i^6)w%t"
DATABASE_URL="postgresql://local_username:local_password@localhost:5555/local_database"
CELERY_BROKER_REDIS_URL="redis://localhost:6555/0"
```

### 4. Create a new TimescaleDB Cloud service:

1. Sign up on [timescaledb](https://www.timescale.com/?utm_source=cfe-github&utm_medium=cfe-repo) to get your production-ready `DATABASE_URL`

2. Under "Services" click "+ Create Service"
3. Select `Time Series and Analytics` as your service type
4. For the configuration:
    - the `Region` so it's near you (e.g. `us-east-1` if you are in New York)
    - `Service name` set it to `django-iot` 
    - all other defaults are fine.
5. Copy the connection string (also known as `Service URL`); this will show the password once in the format: `postgres://tsdbadmin:your-password@yourunique.host-val.tsdb.cloud.timescale.com:37802/tsdb?sslmode=require`
 
### 5. Encrypt `.env.prod`
Next, run:
```bash
ansible-valut encrypt .env.prod
```
Create a password you will remember. To decrypt, you can run `ansible-vault decrypt .env.prod`.

This will ensure your `.env` file does not leak any secrets or passwords.

### 6. Create or update `inventory.ini` in `ansible/`

Check the current inventory file:
```bash
cat ansible/inventory.ini
```

In the repo, it yields:
```ini
[main]
djangopi.local node_id=1

[nodes]
djangopi-2.local node_id=2
djangopi-3.local node_id=3
# djangopi-4.local node_id=4
# djangopi-5.local node_id=5

[all:vars]
ansible_user=cfe
```
Update the amount of nodes as needed.

### 7. Run Connect Hosts 

```bash
cd ansible
ansible-playbook playbooks/connect_hosts.yaml
```
This will make pi-to-pi communication possible. Run this each time you add a new node to the cluster (e.g. a new pi to collect data)

### 8. Push to Prod

From within the `ansible/` directory, run:

```bash
ansible-playbook playbooks/deploy_django.yaml
```
By default, this will install the code from [this repo](https://github.com/codingforentrepreneurs/django-iot-with-timescaledb). If you want to use your own repo, open up `playbooks/deploy_django.yaml` and replace `https://github.com/codingforentrepreneurs/django-iot-with-timescaledb` in the `vars.github_repo:` configuration with your value.

After you push run:

```bash
ansible-playbook playbooks/restart_services.yaml
```


## 9. Refresh Services


```bash
ansible-playbook playbooks/connect_hosts.yaml


ansible-playbook playbooks/deploy_django.yaml


ansible-playbook playbooks/restart_services.yaml
```