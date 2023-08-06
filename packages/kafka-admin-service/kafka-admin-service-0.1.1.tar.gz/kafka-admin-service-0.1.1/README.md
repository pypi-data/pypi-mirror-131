# kafka_admin_service

KAFKA管理类，提供用户创建、删除、列表查询、修改密码，提供主题创建、删除、列表查询，提供权限创建、删除、列表查询等基础管理功能。

## 安装

```
pip install kafka-admin-service
```

## KafkaAdminService类方法

- create_user
- change_password
- get_users
- delete_user
- create_topic
- get_topics
- delete_topic
- add_acl
- delete_acl
- get_acls
- delete_all_topics
- delete_all_users
- create_topic_and_topic_user
- delete_topic_user_acls

## 返回值说明

由于KafkaAdminService在底层以“外部命令调用”的方式调用了kafka/bin/目录下的管理命令，所以返回值中大多会出现returncode/stdout/stderr等字段。其中returncode表示kafka管理命令执行后的退出值，stdout表示kafka管理命令执行后的输出，stderr表示kafka管理命令执行后的错误输出。

## 对于KAFKA服务器配置的要求
1. 要求KAFKA集群使用了scram认证。
1. 要求KAFKA依赖的zookeeper不使用认证。
1. 要求应用运行时的当前目录是Kafka的根目录。
1. 要求已创建正确的./config/scram.jaas文件。
1. 要求已创建正确的./config/scram.client.properties文件。
1. 要求应用服务能正常访问kafka服务器以及zookeeper服务器。

## ./config/scram.jaas模板

```
KafkaServer {
   org.apache.kafka.common.security.scram.ScramLoginModule required
   username="admin"
   password="xxxxxxxx";
};

KafkaClient {
   org.apache.kafka.common.security.scram.ScramLoginModule required
   username="admin"
   password="xxxxxxxx";
};
```

## ./config/scram.client.properties模板

```
security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
```

## 常用的类初始化配置：kafka_admin_service_config.yml

加载配置文件，传递给KafkaAdminService创建方法。

```
zookeeper: localhost:2181
bootstrap_server: localhost:9092
workspace: /apprun/kafka/
command_config_file: "./config/scram.client.properties"
default_kafka_opts: "-Djava.security.auth.login.config=./config/scram.jaas"
topic_partitions: 16
topic_replication_factor: 3
```

## 版本历史

### v0.1.1 2021/12/14

- First Release.
