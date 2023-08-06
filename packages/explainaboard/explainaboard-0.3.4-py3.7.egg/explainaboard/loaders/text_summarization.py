from typing import Dict, Iterable, List
from explainaboard.constants import *
from .loader import register_loader
from .loader import Loader



@register_loader(TaskType.text_summarization)
class TextSummarizationLoader(Loader):
    """
    Validate and Reformat system output file with tsv format:
    text \t true_label \t predicted_label

    usage:
        please refer to `test_loaders.py`
    """

    def load(self) -> Iterable[Dict]:
        """
        :param path_system_output: the path of system output file with following format:
        text \t label \t predicted_label
        :return: class object
        """
        raw_data = self._load_raw_data_points()
        data: List[Dict] = []
        if self._file_type == FileType.tsv:
            for id, dp in enumerate(raw_data):
                source, reference, hypothesis = dp[:3]
                data.append({"id": id,
                             "source": source.strip(),
                             "reference": reference.strip(),
                             "hypothesis": hypothesis.strip()})
        else:
            raise NotImplementedError
        return data