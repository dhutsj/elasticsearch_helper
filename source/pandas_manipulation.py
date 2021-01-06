import pandas as pd
import configparser

cfg_file = "es_helper.ini"
conf = configparser.ConfigParser()
conf.read(cfg_file)
index_field_list = []
for val in conf.items("index_settings"):
    if val[0].__contains__("name"):
        index_name = val[1]
    elif val[0].__contains__("field"):
        index_field_list.append(val[1])


class CsvMani(object):
    def __init__(self, path):
        self.path = path
        self.type = ""

    def judge_tye(self):
        if self.path.__contains__("csv"):
            self.type = "csv"
        elif self.path.__contains__("xltx") or self.path.__contains__("xlsx"):
            self.type = "excel"
        return self.type

    def read_csv(self):
        df = pd.read_csv(self.path, encoding="latin1")
        return df

    def read_excel(self):
        df = pd.read_excel(self.path, encoding="latin1")
        return df

    def convert_to_json_format(self, file_type, index_field_list):
        if file_type == "csv":
            df2 = self.read_csv().dropna()
        elif file_type == "excel":
            df2 = self.read_excel().dropna()
        df3 = df2.to_dict("records")
        print(len(df3))
        for i, data in enumerate(df3):
            yield {
                "_index": index_name,
                "_id": i,
                "_source": {val: data.get(val) for val in index_field_list}
            }
        raise StopIteration


def test():
    cfg_file = "es_helper.ini"
    conf = configparser.ConfigParser()
    conf.read(cfg_file)
    index_field_list = []
    for val in conf.items("index_settings"):
        if val[0].__contains__("name"):
            index_name = val[1]
        elif val[0].__contains__("field"):
            index_field_list.append(val[1])
    print(index_name)
    csv = CsvMani('netflix_titles.csv')
    type = csv.judge_tye()
    # df = csv.read_csv()
    # print(df.head(3))
    # print(df.columns)
    # print(df.shape)
    # print(df["show_id"].nunique())
    # print(df["show_id"])
    # print(df.isnull().sum())
    # df2 = df.dropna()
    # print(df2.isnull().sum())
    # print(df2.shape)
    print(next(csv.convert_to_json_format(type, index_field_list)))


if __name__ == "__main__":
    test()
