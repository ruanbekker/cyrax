# cyrax
Cyrax - a on-demand deploy tool

## Note

This is still under development and in alpha

## Run the server

The server requires docker and docker-compose to be installed:

```
$ python3 -m pip install -r requirements.txt
$ python app.py

 * Debug mode: off
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:8232
 * Running on http://192.168.0.8:8232 (Press CTRL+C to quit)
```

## Usage

Request a environment by passing the url of a docker-compose:

```
$ curl 'http://192.168.0.8:8232/deploy?compose=https://gist.githubusercontent.com/ruanbekker/284c12c85327cf59dedc7546f9a24e38/raw/1b3021d4e4f418380d193b6d1c6deff91583c3d3/docker-compose.yml'
{"app_url":"http://192.168.0.8:36811"}
```

The server finds an open port and binds the open port to the container port defined in the compose file:

```
$ curl http://192.168.0.8:36811/
Hostname: 0de76a27cb5d
```

## Plans

To pass a git repo, stack name and docker compose file, as in:

```json
{
  "repo": "https://github.com/user/my-repo",
  "compose": "docker-compose.yml",
  "stack": "my-stack-name"
}
```

So the repo can be cloned, built and deployed.
