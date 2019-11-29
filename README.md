# project-name

Follow this steps to run this example project:

- have docker instaleld
- run etcd server: https://hub.docker.com/r/bitnami/etcd/
- Build image: docker build -t project-name .
- Run container: docker run --rm --name my_project_container -p 80:80 -e MODULE_NAME="project_name.main" project-name
- go to: http://127.0.0.1:80
- JUST USE DOCKER COMPOSE.

- to run without docker: uvicorn project_name.main:app --reload


# test etcd
>>> etcd = etcd3.client(host='localhost', port=2379)
>>> etcd.put('/project_name/test_x', 'test x var 123')