__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

from labpack.platforms.docker import dockerClient
docker_client = dockerClient()

from labpack.records.settings import load_settings
docker_config = load_settings('../data/test_docker.yaml')

docker_client.enter(docker_config['container_alias'])

docker_client.rm(docker_config['container_alias'])