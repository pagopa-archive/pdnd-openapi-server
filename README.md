# PDND open api server (pre-alpha)

This server exposes API from [PDND](https://dataportal.daf.teamdigitale.it/) according to openapi 3 specification and the interoperability model defined by Italian Governemnt organizations. It uses [connexion](https://github.com/zalando/connexion) framework for creating and exposing the server in a contract first approach. Remember each API is self documented if you want to read the details of each API read the [openapi](https://github.com/teamdigitale/pdnd-openapi-server/blob/master/openapi/daf-openapi.yaml) file or launch the service as described below. 

### Context

The goal of this project is to expose according to openapi 3 standards a set of API developed for [PDND (ex Daf)](http://dataportal.daf.teamdigitale.it). The old API were developed according to swagger 2.0 standards, using Scala. We are now proxying those api throught this repo for becoming compliants with the new standards. Below the list of api we are wrapping:

-  https://github.com/italia/daf-dataportal-backend/blob/master/conf/ftd_api.yaml
- https://github.com/italia/daf-srv-catalog/blob/dev/conf/catalog_manager.yaml
- https://github.com/italia/daf-srv-security/blob/dev/conf/security_manager.yaml

### Prerequisites

On your machine python 3 with pip and [tox](https://tox.readthedocs.io/en/latest/) must be installed

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
tox -e run
```
connect to [http://localhost:8080/pdnd-openapi/ui/](http://localhost:8080/pdnd-openapi/ui/)

### Docker 

Docker MUST be installed on your local machine

```
git clone https://github.com/teamdigitale/pdnd-openapi-server.git
cd pdnd-openapi-server
docker build -t pdnd-openapi-server .
docker run -p 8080:8080 pdnd-openapi-server
```
open your browser at [http://localhost:8080/pdnd-openapi/ui/](http://localhost:8080/pdnd-openapi/ui/)

### Tutorial

The service expose some API from PDND. It requires authentication using Basic Auth or Bearer meaning you as user must be registered [here](https://dataportal.daf.teamdigitale.it/#/register), and must be used respecting the throttling headers defined in accordance with the Linee Guida of the model of interoperability that will be released by the Italian Government organizations.

After registerd you can inser your Email and password:

![Basic Auth](https://raw.githubusercontent.com/teamdigitale/pdnd-openapi-server/master/tutorial/img/basic_auth.png)

Once logged in with basic auth you can get the token as in the image below copy only the jwt value

![Get jwt](https://raw.githubusercontent.com/teamdigitale/pdnd-openapi-server/master/tutorial/img/get_jwt.png)

Copy and paste the jwt and insert it for calling each API:

![Jwt Auth](https://raw.githubusercontent.com/teamdigitale/pdnd-openapi-server/master/tutorial/img/jwt_auth.png)

Now you can call the API as in the image below

![Search API](https://raw.githubusercontent.com/teamdigitale/pdnd-openapi-server/master/tutorial/img/search.png)



