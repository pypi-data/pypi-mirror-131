# kafka_admin_service

Kafka admin service class, provides basic management functions such as USER creation, USER deletion, USER listing all and USER password changing, TOPIC creation, TOPIC deletion, TOPIC listing all, and ACL creation, ACL deletion and ACL listing all.

## Install

```
pip install kafka-admin-service
```

## KafkaAdminService methods

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

## Releases

### v0.1.1 2021/12/14

- First Release.
