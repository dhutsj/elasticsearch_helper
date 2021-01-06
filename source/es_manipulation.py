from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pandas_manipulation import CsvMani
import configparser

cfg_file = "es_helper.ini"
conf = configparser.ConfigParser()
conf.read(cfg_file)
es_host = conf.get("elasticsearch_settings", "elasticsearch_host")
es_port = conf.get("elasticsearch_settings", "elasticsearch_port")


class MyES(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = Elasticsearch([{'host': self.host, 'port': self.port}], timeout=30)

    def create_index(self, index_name, mappings):
        self.connection.indices.create(index=index_name, ignore=400, body=mappings)

    def get_all_indices(self):
        return self.connection.indices.get_alias("*")

    def delete_index(self, index_name):
        self.connection.indices.delete(index=index_name, ignore=[400, 404])

    def upload_json_doc(self, index_name, doc_type=None, json_body=None, doc_id=None):
        """Upload json to es doc

        :param index_name:
        :param doc_type:
        :param json_body:
        :param doc_id:
        :return:

        Usage: e1 = {
        "first_name": "sj",
        "last_name": "tian",
        "age": 20,
        "hobby": ["coding", "cooking"]
        }
        es.index(index="testperson", doc_type="testperson", body=e1, id=1)
        """
        self.connection.index(index=index_name, doc_type=doc_type, body=json_body, id=doc_id)

    def bulk_insert(self, index_generator):
        helpers.bulk(self.connection, index_generator, request_timeout=300)


def csv_to_es(csv_path):
    conf = configparser.ConfigParser()
    conf.read(cfg_file)
    index_field_list = []
    for val in conf.items("index_settings"):
        if val[0].__contains__("field"):
            index_field_list.append(val[1])
    es = MyES(es_host, es_port)
    csv = CsvMani(csv_path)
    type = csv.judge_tye()
    es.bulk_insert(index_generator=csv.convert_to_json_format(type, index_field_list))
    print("bulk inserted")
    # settings_json = {
    #     "settings": {
    #         "number_of_shards": 1,
    #         "number_of_replicas": 0
    #     },
    #     "mappings": {
    #         "properties": {
    #             "title": {"type": "text"},
    #             "director": {"type": "keyword"},
    #             "description": {"type": "text"},
    #             "cast": {"type": "text"},
    #             "type": {"type": "long"}
    #             }
    #         }
    #     }
    # es.create_index(index_name="netflix_movie_manual_mapping_2021_01_05", mappings=settings_json)


if __name__ == "__main__":
    csv_path = "tmp.csv"
    conf = configparser.ConfigParser()
    conf.read(cfg_file)
    es_host = conf.get("elasticsearch_settings", "elasticsearch_host")
    es_port = conf.get("elasticsearch_settings", "elasticsearch_port")
    csv_to_es(csv_path)
