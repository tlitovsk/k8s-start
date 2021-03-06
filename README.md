# INDEX

k8s-start
---------
This will start containers to get a working k8s

container
---------
Directory with definitions for all containers required

manifests
---------
Required by k8s-start to work in privileged mode

specs
-----
Specs to create k8s objects


# START

- Setup k8s on the local host: `setenforce 0 ; bsah get-started`
- Go into the container/controller dir and run the controller
- Use curl to use the controller REST API

# REST API commands

Retrieved using `$ grep route container/controller/controller/__main__.py`

## @app.route('/v1/domains/')
List all available and running domains

    $ curl "127.0.0.1:8084/v1/domains/"
    {"available": ["generic-pxe"], "running": []}

## @app.route('/v1/domains/<name>', method='GET')
Get the domain xml specification

    $ curl "127.0.0.1:8084/v1/domains/generic-pxe"

## @app.route('/v1/domains/<name>/connection/uri', method='GET')
Get the libvirt connection URI (tcp+sasl, without authentication) to the
VM inside the pod.
Each pod will have it's own virtual (cluster) IP.

    $ curl "127.0.0.1:8084/v1/domains/generic-pxe/connection/uri"
    qemu+tcp://10.0.0.42:16509/system

## @app.route('/v1/domains/<name>', method='DELETE')
Delete the domain

    $ curl "127.0.0.1:8084/v1/domains/generic-pxe" -X DELETE

## @app.route('/v1/domains/<name>', method='PUT')
Create the domain, submit the domain xml specification

    $ curl "127.0.0.1:8084/v1/domains/generic-pxe" -X PUT --data @dom.xml

# Depoloyment on Kubernetes

First stet the `externalIP` in
[specs/ovirt-engine-service.json](specs/ovirt-engine-service.json). Then start
the services and pods in the follwing order:

```bash
kubectl create -f specs/ovirt-engine-service.json
kubectl create -f specs/controller-service.json
sleep 10 # Wait for the services to get an IP
kubectl create -f specs/controller-pod.json
kubectl create -f specs/ovirt-engine-pod.json
```

Access the engine with
[https://{externalIp}:8444/ovirt-engine/](https://{externalIp}:8444/ovirt-engine/).
Note that the kubernetes plugin is currently only loaded correctly when you are
logged in to the engine and you see the port number still in the url.
