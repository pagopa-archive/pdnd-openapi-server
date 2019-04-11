# PDND open api server

This server exposes API from [PDND](https://dataportal.daf.teamdigitale.it/) according to openapi 3 specification. It uses [connexion](https://github.com/zalando/connexion) framework for creating and exposing the server.

### Test

To test the API, just run


```
tox 

```

When debugging, you can run the following instead.


```
tox --  --pdb --pdb-failure -vs --nologcapture

```


### Launch

```
pip3 install -r requirements.txt
python3 app.py
```
connect to http://localhost:8080/pdnd-api/ui/

### Docker 

Docker MUST be installed on your local machine

```
git clone https://github.com/teamdigitale/pdnd-openapi-server.git
cd pdnd-openapi-server
docker build -t pdnd-openapi-server .
docker run -p 8080:8080 pdnd-openapi-server
```
open your browser at [http://localhost:8080/pdnd-openapi/ui/](http://localhost:8080/pdnd-openapi/ui/)
