import logging
from .message_utils import produce_message_callback, consume_message_callback
from nubium_utils.metrics import start_pushing_metrics
from .confluent_runtime_vars import env_vars
from nubium_utils.custom_exceptions import WrappedSignals
from nubium_topic_configs.clusters import cluster_topic_map
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
import json
def patched_schema_loads(schema_str):
    from confluent_kafka.schema_registry.avro import Schema
    schema_str = schema_str.strip()
    if schema_str[0] != "{" and schema_str[0] != "[":
        schema_str = '{"type":' + schema_str + '}'

    return Schema(schema_str, schema_type='AVRO')
import confluent_kafka
confluent_kafka.schema_registry.avro._schema_loads = patched_schema_loads


LOGGER = logging.getLogger(__name__)
wrapped_signals = WrappedSignals()  # WrappedSignals needs to be initialized (somewhere) to catch signals


def init_ssl_configs():
    if env_vars()["RHOSAK_USERNAME"]:
        LOGGER.info('Using SASL-authenticated producers/consumers!')
        return {
            "security.protocol": "sasl_ssl",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": env_vars()["RHOSAK_USERNAME"],
            "sasl.password": env_vars()["RHOSAK_PASSWORD"]
        }
    else:
        LOGGER.info('Authentication/encryption disabled for producers/consumers!')
    return {}


def init_schema_registry_configs(as_registry_object=False):
    """
    Provides the avro schema config
    :return: dict, None
    """
    config = None
    if as_registry_object:
        url = 'url'
    else:
        url = 'schema.registry.url'
    LOGGER.info(f'Using the schema server at {env_vars()["SCHEMA_REGISTRY_URL"]}')
    # RHOSAK registry
    if env_vars()['SCHEMA_REGISTRY_USERNAME']:
        config = {url: f"https://{env_vars()['SCHEMA_REGISTRY_SERVER']}"}
        LOGGER.debug(f'Using RHOSAK schema registry config: {config}')
    # local to Bifrost Nubium
    elif env_vars()['SCHEMA_REGISTRY_SSL_CA_LOCATION']:
        config = {
            url: f"https://{env_vars()['SCHEMA_REGISTRY_SERVER']}",
            'ssl.ca.location': env_vars()['SCHEMA_REGISTRY_SSL_CA_LOCATION'],
        }
    # Bifrost Nubium to Bifrost Nubium, local to local
    else:
        config = {url: f"http://{env_vars()['SCHEMA_REGISTRY_SERVER']}"}

    if as_registry_object:
        return SchemaRegistryClient(config)
    else:
        return config


def init_producer_configs(topic, ssl_configs=None, schema_registry_configs=None, cluster=None):
    """
    Sets up a single producer.
    """
    if not ssl_configs:
        ssl_configs = {}
    if not schema_registry_configs:
        schema_registry_configs = {}
    return {
        **ssl_configs,
        **schema_registry_configs,
        "bootstrap.servers": cluster if cluster else cluster_topic_map()[topic],
        "on_delivery": produce_message_callback,
        "acks": "all"}


def producer_serializers(schema_dict, schema_registry):
    return {topic: AvroSerializer(schema_registry, json.dumps(schema)) for topic, schema in schema_dict.items()}


def init_transactional_producer_configs(topic_schema_dict, schema_registry, ssl_configs=None, cluster=None):
    """
    Sets up a single producer.
    """
    if not cluster:
        check_topics = set([topic for topic in topic_schema_dict if topic in cluster_topic_map()])
        unmapped = set(topic_schema_dict.keys()) - check_topics
        if unmapped:
            LOGGER.warning(f'The topic(s) {unmapped} in the provided producer schema dict mapping are not included in'
                           f' the cluster topic map. There are valid use cases for this, such as dynamically adding'
                           f' new topics at runtime with a predetermined schema, or even just testing a new topic on'
                           f' the fly. Either way, make sure this is not a mistake!')
        cluster = set([cluster_topic_map()[topic] for topic in check_topics])
        if len(cluster) == 1:
            cluster = list(cluster)[0]
        else:
            raise ValueError('Cluster count for provided consumer topics did not equal 1. '
                             f'Please confirm your topics are on the same cluster. Topics:\n{topics}')
    if not ssl_configs:
        ssl_configs = {}
    return {
        **ssl_configs,
        "bootstrap.servers": cluster if cluster else cluster_topic_map()[topic],
        "on_delivery": produce_message_callback,
        "key.serializer": AvroSerializer(schema_registry, schema_str="""{"type": "string"}"""),
        "value.serializer": lambda: None,
        "enable.idempotence": "true",
        "transactional.id": env_vars()['HOSTNAME'],
        "acks": "all"}


def init_consumer_configs(topics, ssl_configs=None, schema_registry_configs=None, cluster=None):
    """
    Assummes topics are all in the same cluster.
    """
    if not cluster:
        cluster = set([cluster_topic_map()[topic] for topic in topics])
        if len(cluster) == 1:
            cluster = list(cluster)[0]
        else:
            raise ValueError('Cluster count for provided consumer topics did not equal 1. '
                             f'Please confirm your topics are on the same cluster. Topics:\n{topics}')
    if not ssl_configs:
        ssl_configs = {}
    if not schema_registry_configs:
        schema_registry_configs = {}
    max_time_between_consumes_mins = int(env_vars()['CONSUMER_TIMEOUT_LIMIT_MINUTES']) + int(env_vars()['TIMESTAMP_OFFSET_MINUTES'])
    return {
        **ssl_configs,
        **schema_registry_configs,
        "bootstrap.servers": cluster,
        "group.id": env_vars()['APP_NAME'],
        "group.instance.id": env_vars()['HOSTNAME'],
        "on_commit": consume_message_callback,
        "enable.auto.commit": True if env_vars()['CONSUMER_ENABLE_AUTO_COMMIT']=='true' else False,
        "auto.offset.reset":  'earliest' if env_vars()['CONSUMER_AUTO_OFFSET_RESET']=='earliest' else 'latest',
        "auto.commit.interval.ms": int(env_vars()['CONSUMER_AUTO_COMMIT_INTERVAL_SECONDS']),
        "enable.auto.offset.store": False if env_vars()['CONSUMER_ENABLE_AUTO_COMMIT']=='true' else True,
        "max.poll.interval.ms": 60000 * max_time_between_consumes_mins,
        "session.timeout.ms": int(env_vars()['CONSUMER_HEARTBEAT_TIMEOUT_SECONDS']) * 1000,
        "message.max.bytes": int(env_vars()['MESSAGE_BATCH_MAX_MB']),
        "fetch.max.bytes": int(env_vars()['MESSAGE_TOTAL_MAX_MB']),
        "queued.max.messages.kbytes": int(env_vars()['MESSAGE_QUEUE_MAX_MB'])}


def init_transactional_consumer_configs(topics, schema_registry, ssl_configs=None, cluster=None, schema=None):
    """
    Assummes topics are all in the same cluster.
    """
    if not cluster:
        cluster = set([cluster_topic_map()[topic] for topic in topics])
        if len(cluster) == 1:
            cluster = list(cluster)[0]
        else:
            raise ValueError('Cluster count for provided consumer topics did not equal 1. '
                             f'Please confirm your topics are on the same cluster. Topics:\n{topics}')
    if not ssl_configs:
        ssl_configs = {}
    max_time_between_consumes_mins = int(env_vars()['CONSUMER_TIMEOUT_LIMIT_MINUTES']) + int(env_vars()['TIMESTAMP_OFFSET_MINUTES'])
    # with patch('confluent_kafka.schema_registry.avro._schema_loads', side_effect=patched_schema_loads):
    #     from confluent_kafka.schema_registry.avro import AvroDeserializer

    return {
        # Connection Settings
        **ssl_configs,
        "bootstrap.servers": cluster,

        # General Consumer Settings
        "group.id": env_vars()['APP_NAME'],
        # "group.instance.id": env_vars()['HOSTNAME'],
        "on_commit": consume_message_callback,
        "auto.offset.reset":  'earliest' if env_vars()['CONSUMER_AUTO_OFFSET_RESET']=='earliest' else 'latest',

        # Transaction Settings
        "isolation.level": "read_committed",
        "enable.auto.commit": False,
        "enable.auto.offset.store": False,

        # Registry Serialization Settings
        "key.deserializer": AvroDeserializer(schema_registry, schema_str='{"type": "string"}'),
        "value.deserializer": AvroDeserializer(schema_registry, schema_str=json.dumps(schema) if schema else None),

        # Performance Settings
        "partition.assignment.strategy": 'cooperative-sticky',
        "max.poll.interval.ms": 60000 * max_time_between_consumes_mins,
        "session.timeout.ms": int(env_vars()['CONSUMER_HEARTBEAT_TIMEOUT_SECONDS']) * 1000,
        "message.max.bytes": int(env_vars()['MESSAGE_BATCH_MAX_MB']),
        "fetch.max.bytes": int(env_vars()['MESSAGE_TOTAL_MAX_MB']),
        "queued.max.messages.kbytes": int(env_vars()['MESSAGE_QUEUE_MAX_MB']),
    }


def init_metrics_pushing(metrics_manager):
    if env_vars()['DO_METRICS_PUSHING'].lower() == 'true':
        LOGGER.info('Metric pushing to gateway ENABLED')
        start_pushing_metrics(metrics_manager, int(env_vars()['METRICS_PUSH_RATE']))
    else:
        LOGGER.info('Metric pushing to gateway DISABLED')


def get_kafka_configs():
    return init_ssl_configs(), init_schema_registry_configs()
