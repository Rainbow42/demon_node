import subprocess
import logging

import docker

from conveir.const import PipelinesEnum

logger = logging.getLogger(__name__)


class Pipline:

    def __init__(self):
        self.client = docker.from_env()
        pwd = subprocess.check_output('pwd')
        self.pwd = str(pwd.decode('utf-8')).rstrip()
        self.pwd += "/pipeline/docker_files/"

    def start_build(self):
        # self.client.images.build(
        #     # path=self.pwd,
        #     path='docker_files',
        #     tag='fastapi',
        #     dockerfile='Dockerfile',
        #     nocache=True
        # )
        logger.info("START BUILD")
        container = self.client.containers.run('fastapi', detach=True)

        performed = False
        for line in container.logs(stream=True):
            logger.info(line)
            if 'Application startup complete' in str(line):
                performed = True
                break
        container.stop()
        container.remove()

        return performed

    def start_linter(self) -> bool:
        # self.client.images.build(
        #     # path=self.pwd,
        #     path='docker_files',
        #     dockerfile='Dockerfile.linter',
        #     tag='linter'
        # )
        logger.info("START LINTER")
        container = self.client.containers.run('linter', detach=True)

        performed = ''
        for line in container.logs(stream=True):
            logger.info(line)
            performed += str(line)

        container.stop()
        container.remove()
        # print(performed)

        if performed != '':
            return False
        return True

    def start_tests(self) -> bool:
        # self.client.images.build(
        #     # path=self.pwd,
        #     path='docker_files',
        #     dockerfile='Dockerfile.tests',
        #     tag='tests'
        # )
        logger.info("START TEST")
        container = self.client.containers.run('tests', detach=True)

        performed = True
        for line in container.logs(stream=True):
            logger.info(line)
            if 'failed' in line.decode("utf-8"):
                performed = False

        container.stop()
        container.remove()

        # print(performed)
        return performed

    def start_init(self) -> bool:
        # self.client.images.build(
        #     path=self.pwd,
        #     dockerfile='Dockerfile',
        #     tag='init'
        # )
        # self.client.images.build(
        #     path=self.pwd,
        #     dockerfile='Dockerfile.postgresql',
        #     tag='postgresql_init'
        # )
        logger.info("START INIT")
        cont_init = self.client.containers.run('init', detach=True)
        cont_postgresql = self.client.containers.run('postgresql_init',
                                                     detach=True)

        performed = False
        for line in cont_init.logs(stream=True):
            logger.info(line)
            if 'Application startup complete' in str(line):
                performed = True
                break

        performed_bd = False
        for line in cont_postgresql.logs(stream=True):
            logger.info(line)
            if 'database system is ready to accept connections' in str(line):
                performed_bd = True
                break

        cont_init.stop()
        cont_init.remove()

        cont_postgresql.stop()
        cont_postgresql.remove()

        if performed and performed_bd:
            return True
        return False


class RunPipline(Pipline):
    def run(self, stage) -> bool:
        if stage == PipelinesEnum.BUILD:
            return self.start_build()

        if stage == PipelinesEnum.TESTING:
            return self.start_tests()

        if stage == PipelinesEnum.LINTERS:
            return self.start_linter()

        if stage == PipelinesEnum.INSTALLATION:
            return self.start_init()
