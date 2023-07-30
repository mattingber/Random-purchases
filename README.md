# Random-purchases

A containerized application For managing user purchases of random items.
It is comprised of the following components:

* **mongodb**
* Apache **Kafka** and **Zookeeper** (in a single image)
* A **Kafka UI**
* **scm-api** (server customer management) written in `python`, utilizing `FASTapi`, `Motor` and `AIOKafka`
* **web-gateway** written in python, utilizing `FASTApi` and `AIOKafka`
* **frontend** written in `react`

## deployment

### prerequisites
in order to deploy this application you'll need `git`, `docker` and `docker-compose`

### Running the application
Once you made sure all of the prerequisites are satisfied, follow these steps:
* Clone into the repository

```console
foo@bar:~$ git clone git@github.com:mattingber/Random-purchases.git
foo@bar:~$ cd Random-purchases
```
* Run the compose file

```console
foo@bar:~$ docker-compose up -d --build
```
*Note: the --build flag is necessary for the first run, but not after it, if you don't change anything in the code.*

* Wait and verify that all of the containers are up and healthy
```console
foo@bar:~$ docker-compose ps
frontend      /docker-entrypoint.sh ngin ...   Up             0.0.0.0:80->80/tcp,:::80->80/tcp                                                            
kafka         /bin/sh -c /opt/kafka/bin/ ...   Up (healthy)   0.0.0.0:2181->2181/tcp,:::2181->2181/tcp, 9092/tcp, 0.0.0.0:9093->9093/tcp,:::9093->9093/tcp
kafka-ui      /bin/sh -c java --add-open ...   Up             0.0.0.0:8080->8080/tcp,:::8080->8080/tcp                                                    
mongo         docker-entrypoint.sh mongod      Up             0.0.0.0:27017->27017/tcp,:::27017->27017/tcp                                                
scm-api       python3 main.py                  Up             0.0.0.0:8000->8000/tcp,:::8000->8000/tcp                                                    
web-gateway   python3 main.py                  Up             0.0.0.0:8100->8100/tcp,:::8100->8100/tcp
```
*Notice the health on the kafka container*

### Accessing The Application
Once All of the components are safely running, navigate to [http://localhost](http://localhost/) in your browser to acces the UI.

You can also access scm-api and web-gateway's api documentation at [http://localhost:8000/docs](http://localhost:8000/docs) and [http://localhost:8100/docs](http://localhost:8100/docs), respectably. <br/>
You can also navigate to the kafka UI at [http://localhost:8080](http://localhost:8080)

