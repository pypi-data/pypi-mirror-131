from typing import Dict, Iterable, List
import typing as t
import json
from enum import Enum
from io import StringIO
import csv
from explainaboard.constants import FileType, Source, TaskType

JSON = t.Union[str, int, float, bool, None, t.Mapping[str, 'JSON'], t.List['JSON']] # type: ignore

class Loader:
    """base class of loader"""

    def __init__(self, source: Source, file_type: Enum, data: str):
        self._source = source
        self._file_type = file_type
        self._data = data

    def _load_raw_data_points(self) -> Iterable:
        """
        loads data and return an iterable of data points. element type depends on file_typ
        TODO: error handling
        """
        if self._source == Source.in_memory:
            if self._file_type == FileType.tsv:
                file = StringIO(self._data)
                return csv.reader(file, delimiter='\t')
            raise NotImplementedError

        elif self._source == Source.local_filesystem:
            if self._file_type == FileType.tsv:
                content = []
                with open(self._data, "r") as fin:
                    for record in csv.reader(fin, delimiter='\t'):
                        content.append(record)
                return content
            elif self._file_type == FileType.conll:
                content = []
                with open(self._data, "r") as fin:
                    for record in fin:
                        content.append(record)
                return content
            # elif self._file_type == 'jsonl':
            #     with open(self._data, 'r') as json_file:
            #         json_list = list(json_file)
            #     return json_list
            elif self._file_type == "json":
                with open(self._data, 'r') as json_file:
                    data = json_file.read()
                obj = json.loads(data)
                return obj
            else:
                raise NotImplementedError

    def load(self) -> Iterable[Dict]:
        raise NotImplementedError


# loader_registry is a global variable, storing all basic loading functions
_loader_registry: Dict = {}


def get_loader(task: TaskType, source: Source, file_type: FileType, data: str) -> Loader:
    return _loader_registry[task](source, file_type, data)


def register_loader(task_type: TaskType):
    """
    a register for different data loaders, for example
    For example, `@register_loader(TaskType.text_classification)`
    """
    def register_loader_fn(cls):
        _loader_registry[task_type] = cls
        return cls
    return register_loader_fn







# @register_loader('text_classification')
# class LoadTextClassificationJsonl:
#     """
#     Validate and Reformat system output file with jsonl format:
#     {
#         "text": "I love this movie",
#         "true_label": "positive",
#         "predict_label":"negative"
#     } \n

#     usage:
#         builder = loader_registry['text_classification']['jsonl']()
#         system_output_dict = builder.load(path_system_output = "your_path").system_output
#         system_output_json = builder.load(path_system_output = "your_path").to_json().system_output
#     """

#     def __init__(self, path_system_output: str = None):
#         self._path_system_output: str = path_system_output
#         self._system_output: List[dict] = []

#     def load(self, path_system_output: str = None):
#         """
#         :param path_system_output: the path of system output file with jsonl format
#         :return: class object
#         """
#         self._path_system_output: str = path_system_output
#         self._system_output = []
#         with open(self._path_system_output, encoding="utf8") as fin:
#             for id_, line in enumerate(fin):
#                 jsonl_info = json.loads(line)
#                 text, true_label, predicted_label = jsonl_info["text"], jsonl_info[
#                     "true_label"], jsonl_info["predicted_label"]
#                 self._system_output.append({"id": id_,
#                                             "text": text.strip(),
#                                             "true_label": true_label.strip(),
#                                             "predicted_label": predicted_label.strip()})
#         return self

#     def to_json(self):
#         """
#         :return: class object
#         """
#         self._system_output: JSON = json.dumps(self._system_output, indent=4)
#         return self

#     @property
#     def system_output(self):
#         return self._system_output


