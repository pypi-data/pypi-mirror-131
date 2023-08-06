from daipecore.widgets.Widgets import Widgets
from databricksbundle.detector import is_databricks
from pyspark.dbutils import DBUtils

import re


class DatabricksWidgets(Widgets):
    def __init__(self, dbutils: DBUtils):
        self.__dbutils = dbutils
        self.__multiselect_fields = []
        self.__widget_index = 0
        self.__name_validator = re.compile("^[a-z][a-z_0-9]+$")

    def __generate_widget_label(self, name):
        if self.__name_validator.match(name) is None:
            raise Exception("The name you provided is incorrect, please provide name containing only alpha-numeric letters and _")

        self.__widget_index = self.__widget_index + 1

        widget_number_str = f"{self.__widget_index:02d}. "

        return widget_number_str + name.replace("_", " ")

    def add_text(self, name: str, default_value: str = "", label: str = None):
        default_value = default_value if default_value is not None else ""
        label = self.__generate_widget_label(name) if label is None else label

        self.__dbutils.widgets.text(name, default_value, label)

    def add_select(self, name: str, choices: list, default_value: str, label: str = None):
        if None in choices:
            raise Exception("Value None cannot be used as choice, use empty string instead")

        if default_value not in choices:
            raise Exception(f'Default value "{default_value}" not among choices')

        label = self.__generate_widget_label(name) if label is None else label

        self.__dbutils.widgets.dropdown(name, default_value, choices, label)

    def add_multiselect(self, name: str, choices: list, default_values: list, label: str = None):
        if None in choices:
            raise Exception("Value None cannot be used as choice, use empty string instead")

        label = self.__generate_widget_label(name) if label is None else label

        self.__multiselect_fields.append(name)
        self.__dbutils.widgets.multiselect(name, default_values, choices, label)

    def remove(self, name: str):
        self.__dbutils.widgets.remove(name)

    def remove_all(self):
        self.__dbutils.widgets.removeAll()
        self.__widget_index = 0

    def get_value(self, name: str):
        value = self.__dbutils.widgets.get(name)

        if name in self.__multiselect_fields:
            if value == "":
                return []

            return value.split(",")

        return value

    def should_be_resolved(self):
        return is_databricks()
