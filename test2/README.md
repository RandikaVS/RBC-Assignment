
## TEST 2: Ansible Automation


1. The solution follows infrastructure-as-code (IaC) principles, making system checks and service management repeatable, consistent, and version-controlled.

2. The use of a centralized inventory file allows easy grouping of hosts and enables the same playbook to scale across multiple environments with minimal changes.

3. Action-based execution using variables (action) ensures flexibility, allowing selective task execution without modifying the playbook logic.
4. The playbook is modular and readable, with clearly separated tasks for service verification, disk monitoring, and application health checks.

5. Conditional execution and thresholds reduce unnecessary operations and ensure alerts are triggered only when required.

6. Built-in handler support enables controlled service restarts, improving reliability while avoiding unnecessary disruptions.

7. The solution is extensible, allowing additional services, checks, or alert mechanisms to be added with minimal effort.

8. The design supports automation-first operations, reducing manual intervention and improving operational efficiency.


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