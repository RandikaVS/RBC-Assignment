# RBC Assignment

This repository contains the solutions for the RBC assignment, divided into three tests.

## Prerequisites

- Python 3.8+
- Ansible 2.9+
- Linux environment (or macOS for development/testing)

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## TEST 1: Service Monitoring & REST API

This solution consists of a Python REST web service and a monitoring script.

### 1. Start the REST API Service

The service runs on FastAPI.

```bash
cd test1
fastapi dev main.py
```

The API will be available at:

- **Healthcheck**: [http://127.0.0.1:8000/v1/healthcheck](http://127.0.0.1:8000/v1/healthcheck)
- **Add Status**: POST [http://127.0.0.1:8000/v1/add](http://127.0.0.1:8000/v1/add)
- **Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Run the Monitoring Script

In a separate terminal (with venv activated), run the monitor script. This script checks the status of `httpd`, `rabbitmq-server`, and `postgresql`, saves the status to a JSON file in `test1/data`, and automatically uploads it to the running API.

```bash
# Must be run from the root directory or adjust python path
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 test1/src/services/monitor_services.py
```

_Note: Ensure the API is running before executing the monitor script._

---

## TEST 2: Ansible Automation

This solution uses Ansible playbooks to manage services and check system status.

**Inventory File**: `test2/inventory.ini` defines the host groups. Update `ansible_host` and `ansible_user` as needed for your environment.

### Commands

1. **Verify & Install Services**:
   Checks if services (e.g., httpd) are installed on their respective hosts and installs them if missing.

   ```bash
   cd test2
   ansible-playbook playbook.yml -i inventory.ini -e action=verify_install
   ```

2. **Check Disk Usage**:
   Checks if disk usage is > 80% and sends an email alert.

   ```bash
   cd test2
   ansible-playbook playbook.yml -i inventory.ini -e action=check-disk
   ```

3. **Check Application Status**:
   Queries the REST API (from Test 1) to get the application status. Ensure the API from Test 1 is running.
   ```bash
   cd test2
   ansible-playbook playbook.yml -i inventory.ini -e action=check-status
   ```

---

## TEST 3: Data Processing

This solution processes a CSV file to filter properties sold for less than the average price per square foot.

```bash
cd test3
python3 main.py
```

**Output**: A new file named `sales_below_avg.csv` will be generated in the `test3` directory.
