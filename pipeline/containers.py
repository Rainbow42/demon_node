import subprocess

import docker

# from conveir.const import PipelinesEnum


class Pipline:

    def __init__(self):
        self.client = docker.from_env()

    def start_build(self):
        pwd = subprocess.check_output('pwd')
        pwd = str(pwd.decode('utf-8')).rstrip()
        pwd += "/docker_files/"

        self.client.images.build(path='docker_files', tag='fastapi',
                                 dockerfile='Dockerfile', nocache=True)
        container = self.client.containers.run('fastapi', detach=True)

        performed = False
        for line in container.logs(stream=True):
            if 'Application startup complete' in str(line):
                performed = True
                break

        container.stop()
        container.remove()

        return performed

    def start_linter(self) -> bool:
        self.client.images.build(
            path='docker_files',
            dockerfile='Dockerfile.linter',
            tag='linter'
        )
        container = self.client.containers.run('linter', detach=True)

        performed = ''
        for line in container.logs(stream=True):
            performed += str(line)

        container.stop()
        container.remove()
        print(performed)
        self.client.images.remove('linter')

        if performed != '':
            return False
        return True

    def start_tests(self) -> bool:
        self.client.images.build(
            path='docker_files',
            dockerfile='Dockerfile.tests',
            tag='tests'
        )
        container = self.client.containers.run('tests', detach=True)

        performed = True
        for line in container.logs(stream=True):
            print(line)
            if 'failed' in line.decode("utf-8"):
                performed = False

        container.stop()
        container.remove()
        # self.client.images.remove('tests')
        print(performed)
        return performed

    def start_init(self) -> bool:
        self.client.images.build(
            path='docker_files/init',
            dockerfile='Dockerfile',
            tag='init'
        )
        self.client.images.build(
            path='docker_files/init',
            dockerfile='Dockerfile.postgresql',
            tag='postgresql_init'
        )
        cont_init = self.client.containers.run('init', detach=True)
        cont_postgresql = self.client.containers.run('postgresql_init',
                                                     detach=True)

        performed = False
        for line in cont_init.logs(stream=True):
            if 'Application startup complete' in str(line):
                performed = True
                break

        performed_bd = False
        for line in cont_postgresql.logs(stream=True):
            if 'database system is ready to accept connections' in str(line):
                performed_bd = True
                break

        # cont_init.stop()
        # cont_init.remove()

        # self.client.images.remove('tests')
        print(performed_bd)
        if performed and performed_bd:
            return True
        return False


# class RunPipline(Pipline):
#     def run(self, stage) -> bool:
#         if stage == PipelinesEnum.BUILD:
#             return self.start_build()
#
#         if stage == PipelinesEnum.TESTING:
#             return self.start_tests()
#
#         if stage == PipelinesEnum.LINTERS:
#             return self.start_linter()
#
#         if stage == PipelinesEnum.INSTALLATION:
#             return self.start_init()


Pipline().start_linter()
