from typing import Iterable
from explainaboard import feature
from explainaboard.constants import TaskType
from explainaboard.processors.processor import Processor
from explainaboard.processors.processor_registry import register_processor
from explainaboard.builders.text_summarization import SummExplainaboardBuilder

@register_processor(TaskType.text_summarization)
class TextSummarizationProcessor(Processor):
    _task_type = TaskType.text_summarization
    _features = feature.Features({
        "source": feature.Value("string"),
        "reference": feature.Value("string"),
        "hypothesis": feature.Value("string"),
        "attr_source_len": feature.Value(dtype="float",
                                         is_bucket=True,
                                         bucket_info=feature.BucketInfo(
                                             _method="bucket_attribute_specified_bucket_value",
                                             _number=4,
                                             _setting=())),
        "attr_compression": feature.Value(dtype="float",
                                         is_bucket=True,
                                         bucket_info=feature.BucketInfo(
                                             _method="bucket_attribute_specified_bucket_value",
                                             _number=4,
                                             _setting=())),
        "attr_copy_len": feature.Value(dtype="float",
                                          is_bucket=True,
                                          bucket_info=feature.BucketInfo(
                                              _method="bucket_attribute_specified_bucket_value",
                                              _number=4,
                                              _setting=())),
        "attr_coverage": feature.Value(dtype="float",
                                       is_bucket=True,
                                       bucket_info=feature.BucketInfo(
                                           _method="bucket_attribute_specified_bucket_value",
                                           _number=4,
                                           _setting=())),
        "attr_novelty": feature.Value(dtype="float",
                                       is_bucket=True,
                                       bucket_info=feature.BucketInfo(
                                           _method="bucket_attribute_specified_bucket_value",
                                           _number=4,
                                           _setting=()))

    })


    def __init__(self, metadata: dict, system_output_data: Iterable[dict]) -> None:
        super().__init__(metadata, system_output_data)
        self._builder = SummExplainaboardBuilder(self._system_output_info, system_output_data)