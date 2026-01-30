
## TEST 1: Service Monitoring & REST API

1. This solution consists of a FastAPI REST API and a monitoring script. The API provides endpoints to add service status and retrieve service status. 

2. The monitoring script checks the status of `httpd`, `rabbitmq-server`, and `postgresql`, saves the status to a JSON file in `test1/data`, and automatically uploads it to the running API. 

3. The API is available at `http://127.0.0.1:8000/v1/healthcheck`. The API also provides a `docs` endpoint at `http://127.0.0.1:8000/docs` to view the API documentation. 

4. Folders and files are well structured and organized to keep the code clean and maintainable.

5. test1/main.py file is the entry point of the application. It is a FastAPI application that provides endpoints to add service status and retrieve service status. And middleware + initialization doing in this file.

6. When server starts monitor script will run automatically and check the status of `httpd`, `rabbitmq-server`, and `postgresql`, saves the status to a JSON file in `test1/data`.

7. api/v1/endpoints.py file is the entry point of the API. It's including "/add" and "/healthcheck" endpoints. and Elasticsearch connection doing in this file and it's using inside the endpoint to index and retrieve data from Elasticsearch.

8. src/services/el_search_service.py file is the Elasticsearch service. It's including Elasticsearch connection and it's using inside the endpoint to index and retrieve data from Elasticsearch.

9. src/config/settings.py file is the settings file. It's including Elasticsearch connection and it's using inside the endpoint to index and retrieve data from Elasticsearch.

10. src/config/logger.py file is the logger file. It's including logger configuration and it's using inside the endpoint to index and retrieve data from Elasticsearch. 

11. src/models/models.py file is the models file. It's including models for the API endpoints.

---------------------------------------------------------------------------------------------------------------------------

###### 1. Start the REST API Service ######

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

