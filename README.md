# FOSS4G Europe Elasticsearch and Kibana workshop

## Objectives

## Set up

```bash
curl -fsSL https://elastic.co/start-local > start-local
bash start-local -v 9.0.3
```

You'll see how images are downloaded, volumes and containers created, etc.

```text
🎉 Congrats, Elasticsearch and Kibana are installed and running in Docker!

🌐 Open your browser at http://localhost:5601

   Username: elastic
   Password: hODGZcFs

🔌 Elasticsearch API endpoint: http://localhost:9200
🔑 API key: Uko2eXk1Y0JQd19WX2N3dVdiY0c6YUpvMGdFc3lTSnZlU2FfRXF2Uk1jZw==

Learn more at https://github.com/elastic/start-local
```

Copy the login details from the command output:

* User and password
* API key

Now you can add the following code to the `elastic-start-local/docker-compose.yml` file, just after the Kibana service is defined and before the `volumes` key.

```yaml
  notebook:
    depends_on:
      elasticsearch:
        condition: service_healthy
      kibana:
        condition: service_healthy
    image: quay.io/jupyter/base-notebook
    volumes:
      - ../lab:/lab
    working_dir: /lab
    ports:
      - 127.0.0.1:8888:8888
    environment:
      - ES_URL=http://elasticsearch:9200
      - KB_URL=http://kibana:${KIBANA_LOCAL_PORT}
      - ES_PASS=${ES_LOCAL_PASSWORD}
    command: start-notebook.py --NotebookApp.token='elastic'
```

Stop and start the services with the scripts provided in the `elastic-start-local` folder to get the Jupyterlab environment ready at <http://localhost:8888/lab?token=elastic>.

## Juyterlab notebook: downloading data and interacting with Elasticsearch and Kibana programatically

In the Jupyterlab UI, open the `lab/download_and_ingest.ipynb` notebook to continue the lab.

## Kibana


Now you can open Kibana at <http://localhost:5601> and start using the stack from the UI. Remember the password for the `elastic` user was shared when you installed the components. For example, head to the "Dev Tools" interface to keep making API calls to Elasticsearch or Kibana.
