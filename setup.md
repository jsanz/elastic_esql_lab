# Set up

You can run this workshop in three different ways:

* Run a Elastic stack (Elasticsearch & Kibana) on your computer
* Using an Elastic stack deployment in [Elastic Cloud](https://cloud.elastic.co) or anywhere else
* With an [Elastic Serverless project](https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/serverless)

The following instructions set up a local environment with Elasticsearch and Kibana.

Create a new folder and inside execute the following commands to download the `start-local` script and execute it:

```bash
curl -fsSL https://elastic.co/start-local > start-local
bash start-local -v 9.0.3
```

For more details about `start-local` refer to the [README on GitHub](https://github.com/elastic/start-local).

You'll see how images are downloaded, volumes and containers created, etc. An output like this will be rendered at the end of the execution:

```text
🎉 Congrats, Elasticsearch and Kibana are installed and running in Docker!

🌐 Open your browser at http://localhost:5601

   Username: elastic
   Password: hODGZcFs

🔌 Elasticsearch API endpoint: http://localhost:9200
🔑 API key: OThOSDJwY0I3QnlxdzlfMnVtZTc6TDlSUlpCVjRoQXdvb0oyODVNaVFEUQ==

Learn more at https://github.com/elastic/start-local
```

Copy the login details from the command output:

* User and password
* API key


## Add a Jupyterlab notebook environment

Now you can add the following code to the `elastic-start-local/docker-compose.yml` file,
just after the Kibana service is defined and before the `volumes` key.

```yaml
  notebook:
    depends_on:
      elasticsearch:
        condition: service_healthy
      kibana:
        condition: service_healthy
    build:
      context: ..
      dockerfile: notebook.dockerfile
    volumes:
      - ../lab:/lab
    ports:
      - 127.0.0.1:8888:8888
    environment:
      - ES_URL=${ES_URL}
      - KB_URL=${KB_URL}
      - ES_APIKEY=${ES_APIKEY}
      - ES_USER=${ES_USER}
      - ES_PASS=${ES_PASS}
```

And the new required environment variables in the `elastic-start-local/.env` file:

```ini
# local
ES_URL=http://elasticsearch:9200
KB_URL=http://kibana:${KIBANA_LOCAL_PORT}
ES_APIKEY=${ES_LOCAL_API_KEY}
ES_USER=elastic
ES_PASS=${ES_LOCAL_PASSWORD}
```

### Using a separate Elastic stack or Elastic Serverless

If you want to use any other Elastic stack like a Elastic Cloud hosted environment
you can modify the environment variables in the `.env` accordingly.

Stop and start the services with the scripts provided in the `elastic-start-local` 
folder to get the Jupyterlab environment ready at 

## Check the Notebook and Kibana

* Jupyterlab URL: <http://localhost:8888/lab?token=elastic>.
* Kibana URL: <http://localhost:5601>
