import os
import re
import typing
import subprocess
import logging
import platform

logger = logging.getLogger(__name__)

class KafkaAdminService(object):
    """
    1. You must setup your kafka instance with scram authenticate.
    2. You are using zookeeper without authenticate.
    3. You must make sure you are working at kafka's root folder.
    4. You must have an GOOD ./config/scram.jaas.
    5. You must have an GOOD ./config/scram.client.properties.
    6. You can access both zookeeper and kafka on your application server.
    """

    class Operations:
        Describe = "DESCRIBE"
        DescribeConfigs = "DESCRIBE_CONFIGS"
        Alter = "ALTER"
        Read = "READ"
        Delete = "DELETE"
        Create = "CREATE"
        All = "ALL"
        Write = "WRITE"
        AlterConfigs = "ALTER_CONFIGS"

    default_kafka_configs_cmd = "./bin/kafka-configs.sh"
    default_kafka_topics_cmd = "./bin/kafka-topics.sh"
    default_kafka_acls_cmd = "./bin/kafka-acls.sh"
    default_command_config_file = "./config/scram.client.properties"
    default_kafka_opts = "-Djava.security.auth.login.config=./config/scram.jaas"

    default_topic_partitions = 16
    default_topic_replication_factor = 3
    default_create_user_cmd_template = """{kafka_configs_cmd} --zookeeper {zookeeper} --alter --add-config 'SCRAM-SHA-256=[password={password}],SCRAM-SHA-512=[password={password}]' --entity-type users --entity-name {username}"""
    default_get_users_cmd_template = """{kafka_configs_cmd} --zookeeper {zookeeper} --describe  --entity-type users"""
    default_delete_user_cmd_template = """{kafka_configs_cmd} --zookeeper {zookeeper} --alter --delete-config SCRAM-SHA-256,SCRAM-SHA-512 --entity-type users --entity-name {username}"""
    default_create_topic_cmd_template = """{kafka_topics_cmd} --zookeeper {zookeeper} --create --topic {topic_name} --partitions {topic_partitions} --replication-factor {topic_replication_factor}"""
    default_get_topics_cmd_template = """{kafka_topics_cmd} --zookeeper {zookeeper} --list"""
    default_delete_topic_cmd_template = """{kafka_topics_cmd} --zookeeper {zookeeper} --delete --topic {topic_name} --force"""
    default_add_acl_cmd_template = """{kafka_acls_cmd} --bootstrap-server {bootstrap_server} --command-config {command_config_file} --add --topic {topic_name} --allow-principal User:{username} --operation {operation} --force"""
    default_get_acls_cmd_template = """{kafka_acls_cmd} --bootstrap-server {bootstrap_server} --command-config {command_config_file} --list"""
    default_delete_acl_cmd_template = """{kafka_acls_cmd} --bootstrap-server {bootstrap_server} --command-config {command_config_file} --remove --topic {topic_name} --allow-principal User:{username} --operation {operation} --force"""

    def get_default_zookeeper(self):
        return "{hostname}:2181".format(hostname=platform.node())

    def get_default_bootstrap_server(self):
        return "{hostname}:9092".format(hostname=platform.node())

    def get_default_workspace(self):
        return os.getcwd()

    def is_file_exists(self, filename):
        filename = os.path.join(self.workspace, filename)
        return os.path.exists(filename)

    def __init__(self, config=None):
        self.config = config or {}

        self.create_user_cmd_template = self.config.get("create_user_cmd_template", self.default_create_user_cmd_template)
        self.get_users_cmd_template = self.config.get("get_users_cmd_template", self.default_get_users_cmd_template)
        self.delete_user_cmd_template = self.config.get("delete_user_cmd_template", self.default_delete_user_cmd_template)
        self.create_topic_cmd_template = self.config.get("create_topic_cmd_template", self.default_create_topic_cmd_template)
        self.get_topics_cmd_template = self.config.get("get_topics_cmd_template", self.default_get_topics_cmd_template)
        self.delete_topic_cmd_template = self.config.get("delete_topic_cmd_template", self.default_delete_topic_cmd_template)
        self.add_acl_cmd_template = self.config.get("add_acl_cmd_template", self.default_add_acl_cmd_template)
        self.get_acls_cmd_template = self.config.get("get_acls_cmd_template", self.default_get_acls_cmd_template)
        self.delete_acl_cmd_template = self.config.get("delete_acl_cmd_template", self.default_delete_acl_cmd_template)

        self.kafka_configs_cmd = self.config.get("kafka_configs_cmd", self.default_kafka_configs_cmd)
        self.kafka_topics_cmd = self.config.get("kafka_topics_cmd", self.default_kafka_topics_cmd)
        self.kafka_acls_cmd = self.config.get("kafka_acls_cmd", self.default_kafka_acls_cmd)

        self.zookeeper = self.config.get("zookeeper", self.get_default_zookeeper())
        self.bootstrap_server = self.config.get("bootstrap_server", self.get_default_bootstrap_server())
        self.kafka_opts = self.config.get("kafka_opts", self.default_kafka_opts)
        self.command_config_file = self.config.get("command_config_file", self.default_command_config_file)

        self.cmd_execute_timeout = self.config.get("cmd_execute_timeout", 30)
        self.topic_partitions = self.config.get("topic_partitions", self.default_topic_partitions)
        self.topic_replication_factor = self.config.get("topic_replication_factor", self.default_topic_replication_factor)

        self.workspace = self.config.get("workspace", self.get_default_workspace())

        if not self.is_file_exists(self.kafka_configs_cmd):
            logger.error(f"kafka_configs_cmd {self.kafka_configs_cmd} not exists...")
        
        if not self.is_file_exists(self.kafka_topics_cmd):
            logger.error(f"kafka_topics_cmd {self.kafka_topics_cmd} not exists...")

        if not self.is_file_exists(self.kafka_acls_cmd):
            logger.error(f"kafka_acls_cmd {self.kafka_acls_cmd} not exists...")

        if not self.is_file_exists(self.command_config_file):
            logger.error(f"command_config_file {self.command_config_file} not exists...")

        scram_jaas = re.findall("-Djava.security.auth.login.config=([^\ ]*)", self.kafka_opts)[0]
        if not self.is_file_exists(scram_jaas):
            logger.error(f"scram_jaas {scram_jaas} not exists...")
        
    
    def execute(self, cmd, kafka_opts=None)  -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        if kafka_opts:
            extra_env = os.environ
            extra_env["KAFKA_OPTS"] = kafka_opts
            proc = subprocess.Popen(cmd, shell=True, universal_newlines=True, cwd=self.workspace, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=extra_env)
        else:
            proc = subprocess.Popen(cmd, shell=True, universal_newlines=True, cwd=self.workspace, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(timeout=self.cmd_execute_timeout)
        return proc.returncode, stdout, stderr

    def update_user(self, username, password) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        cmd = self.create_user_cmd_template.format(
            kafka_configs_cmd = self.kafka_configs_cmd,
            zookeeper = self.zookeeper,
            username = username,
            password = password,
        )
        return self.execute(cmd)

    def create_user(self, username, password) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        return self.update_user(username, password)

    def change_password(self, username, password) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        return self.update_user(username, password)

    def get_users(self) -> typing.Tuple[int, list, str, str]:
        """Returns [returncode, users, stdout, stderr]
        """
        cmd = self.get_users_cmd_template.format(
            kafka_configs_cmd = self.kafka_configs_cmd,
            zookeeper = self.zookeeper,
        )
        returncode, stdout, stderr = self.execute(cmd)
        if returncode == 0:
            users = re.findall("""Configs for user-principal '(.*)' are""", stdout)
            return returncode, users, stdout, stderr
        else:
            return returncode, [], stdout, stderr

    def delete_user(self, username) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        cmd = self.delete_user_cmd_template.format(
            kafka_configs_cmd = self.kafka_configs_cmd,
            zookeeper = self.zookeeper,
            username = username,
        )
        return self.execute(cmd)

    def create_topic(self, topic_name, topic_partitions=None, topic_replication_factor=None) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        topic_partitions = topic_partitions or self.topic_partitions
        topic_replication_factor = topic_replication_factor or self.topic_replication_factor
        cmd = self.create_topic_cmd_template.format(
            kafka_topics_cmd = self.kafka_topics_cmd,
            zookeeper = self.zookeeper,
            topic_name = topic_name,
            topic_partitions = topic_partitions,
            topic_replication_factor = topic_replication_factor,
        )
        return self.execute(cmd)

    def get_topics(self) -> typing.Tuple[int, list, str, str]:
        """Returns [returncode, topics, stdout, stderr]"""
        cmd = self.get_topics_cmd_template.format(
            kafka_topics_cmd = self.kafka_topics_cmd,
            zookeeper = self.zookeeper,
        )
        returncode, stdout, stderr = self.execute(cmd)
        if returncode == 0:
            topics = stdout.splitlines()
            return returncode, topics, stdout, stderr
        else:
            return returncode, [], stdout, stderr

    def delete_topic(self, topic_name) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        cmd = self.delete_topic_cmd_template.format(
            kafka_topics_cmd = self.kafka_topics_cmd,
            zookeeper = self.zookeeper,
            topic_name = topic_name,
        )
        return self.execute(cmd)

    def add_acl(self, topic_name, username, operation) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        cmd = self.add_acl_cmd_template.format(
            kafka_acls_cmd = self.kafka_acls_cmd,
            bootstrap_server = self.bootstrap_server,
            command_config_file = self.command_config_file,
            topic_name = topic_name,
            username = username,
            operation = operation,  
        )
        return self.execute(cmd, kafka_opts=self.kafka_opts)

    def delete_acl(self, topic_name, username, operation) -> typing.Tuple[int, str, str]:
        """Returns [returncode, stdout, stderr]"""
        cmd = self.delete_acl_cmd_template.format(
            kafka_acls_cmd = self.kafka_acls_cmd,
            bootstrap_server = self.bootstrap_server,
            command_config_file = self.command_config_file,
            topic_name = topic_name,
            username = username,
            operation = operation,  
        )
        return self.execute(cmd, kafka_opts=self.kafka_opts)

    def get_acls(self) -> typing.Tuple[int, list, str, str]:
        """Returns [returncode, users, stdout, stderr]"""
        cmd = self.get_acls_cmd_template.format(
            kafka_acls_cmd = self.kafka_acls_cmd,
            bootstrap_server = self.bootstrap_server,
            command_config_file = self.command_config_file,
        )
        returncode, stdout, stderr = self.execute(cmd)

        acls = {}
        if returncode == 0:
            current_topic_name = None
            current_topic_acls = {}
            for line in stdout.splitlines():
                if line.startswith("Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name="):
                    current_topic_name = re.findall("name=(.*), patternType=", line)[0]
                    if current_topic_name and (not current_topic_name in acls):
                        acls[current_topic_name] = {}
                    current_topic_acls = acls[current_topic_name]
                else:
                    acl_pairs = re.findall("principal=User:(.*), host=\*, operation=(.*), permissionType=ALLOW", line)
                    
                    for username, operation in acl_pairs:
                        if not username in current_topic_acls:
                            current_topic_acls[username] = []
                        current_topic_acls[username].append(operation)

        return returncode, acls, stdout, stderr

    def delete_all_topics(self):
        deleted_topics = []
        errors = {}
        returncode, topics, stdout, stderr = self.get_topics()
        if returncode == 0:
            for topic_name in topics:
                returncode, stdout, stderr = self.delete_topic(topic_name)
                if returncode == 0:
                    deleted_topics.append(topic_name)
                else:
                    errors["topic_name"] = {
                        "stdout": stdout,
                        "stderr": stderr,
                    }
        else:
            errors["_get_topics"] = {
                "stdout": stdout,
                "stderr": stderr,
            }
        return {
            "deleted_topics": deleted_topics,
            "errors": errors,
        }

    def delete_all_users(self, preserves="admin"):
        deleted_users = []
        errors = {}
        if isinstance(preserves, str):
            preserves = [preserves]
        returncode, users, stdout, stderr = self.get_users()
        if returncode == 0:
            for user in users:
                if user in preserves:
                    continue
                returncode, stdout, stderr = self.delete_user(user)
                if returncode == 0:
                    deleted_users.append(user)
                else:
                    errors[user] = {
                        "stdout": stdout,
                        "stderr": stderr,
                    }
        else:
            errors["_get_users"] = {
                "stdout": stdout,
                "stderr": stderr,
            }
        return {
            "deleted_users": deleted_users,
            "preserves": preserves,
            "errors": errors,
        }

    def create_topic_and_topic_user(self, topic_name, username, password, topic_partitions=None, topic_replication_factor=None):
        """Create a topic, create an user, and give read,write,describe acls to the user on the topic."""
        create_topic_returncode, create_topic_stdout, create_topic_stderr = self.create_topic(topic_name, topic_partitions, topic_replication_factor)
        create_user_returncode, create_user_stdout, create_user_stderr = self.create_user(username, password)
        add_read_acl_returncode, add_read_acl_stdout, add_read_acl_stderr = self.add_acl(topic_name, username, self.Operations.Read)
        add_write_acl_returncode, add_write_acl_stdout, add_write_acl_stderr = self.add_acl(topic_name, username, self.Operations.Write)
        add_describe_acl_returncode, add_describe_acl_stdout, add_describe_acl_stderr = self.add_acl(topic_name, username, self.Operations.Describe)

        return {
            "returncode": create_topic_returncode + create_user_returncode + add_read_acl_returncode + add_write_acl_returncode + add_describe_acl_returncode,
            "returncodes": {
                "create_topic": create_topic_returncode,
                "create_user": create_user_returncode,
                "add_read_acl": add_read_acl_returncode,
                "add_write_acl": add_write_acl_returncode,
                "add_describe_acl": add_describe_acl_returncode,
            },
            "stdout": {
                "create_topic": create_topic_stdout,
                "create_user": create_user_stdout,
                "add_read_acl": add_read_acl_stdout,
                "add_write_acl": add_write_acl_stdout,
                "add_describe_acl": add_describe_acl_stdout,
            },
            "stderr": {
                "create_topic": create_topic_stderr,
                "create_user": create_user_stderr,
                "add_read_acl": add_read_acl_stderr,
                "add_write_acl": add_write_acl_stderr,
                "add_describe_acl": add_describe_acl_stderr,
            }
        }

    def delete_topic_user_acls(self, topic_name, username):
        """Delete all the user's acls on the given topic"""
        deleted_acls = []
        errors = {}
        returncode, acls, stdout, stderr = self.get_acls()
        if returncode == 0:
            ops = acls.get(topic_name, {}).get(username, [])
            for op in ops:
                returncode, stdout, stderr = self.delete_acl(topic_name, username, op)
                if returncode == 0:
                    deleted_acls.append((topic_name, username, op))
                else:
                    errors[op] = {
                        "stdout": stdout,
                        "stderr": stderr,
                    }
        else:
            errors["_get_acls"] = {
                "stdout": stdout,
                "stderr": stderr,
            }
        return {
            "topic_name": topic_name,
            "username": username,
            "deleted_acls": deleted_acls,
            "errors": errors,
        }
