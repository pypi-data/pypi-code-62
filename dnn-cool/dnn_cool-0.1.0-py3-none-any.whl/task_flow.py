from typing import Iterable, Optional, Callable, Tuple, Any

import torch
import os

from dataclasses import dataclass, field
from torch import nn
from torch.utils.data import Dataset

from dnn_cool.activations import CompositeActivation
from dnn_cool.datasets import FlowDataset, LeafTaskDataset
from dnn_cool.decoders import BinaryDecoder, TaskFlowDecoder, Decoder, ClassificationDecoder, \
    MultilabelClassificationDecoder
from dnn_cool.evaluation import EvaluationCompositeVisitor, EvaluationVisitor
from dnn_cool.filter import FilterCompositeVisitor, FilterVisitor
from dnn_cool.losses import TaskFlowLoss, ReducedPerSample
from dnn_cool.metrics import TorchMetric, BinaryAccuracy, ClassificationAccuracy, \
    ClassificationF1Score, ClassificationPrecision, ClassificationRecall, BinaryF1Score, \
    BinaryPrecision, BinaryRecall, MeanAbsoluteError, MultiLabelClassificationAccuracy, get_default_binary_metrics, \
    get_default_bounded_regression_metrics, get_default_classification_metrics, \
    get_default_multilabel_classification_metrics
from dnn_cool.missing_values import positive_values, positive_values_unsqueezed, has_no_missing_labels
from dnn_cool.modules import SigmoidAndMSELoss, Identity, TaskFlowModule
from dnn_cool.treelib import TreeExplainer


class ITask:

    def __init__(self, name: str, inputs, available_func=None, metrics: Tuple[str, TorchMetric] = ()):
        self.name = name
        self.inputs = inputs
        self.available_func = available_func
        self.metrics = metrics

    def get_name(self):
        return self.name

    def get_activation(self) -> Optional[nn.Module]:
        return None

    def get_decoder(self):
        return None

    def get_filter(self):
        return FilterVisitor(self, prefix='')

    def get_evaluator(self):
        return EvaluationVisitor(self, prefix='')

    def has_children(self):
        return False

    def get_available_func(self):
        return self.available_func

    def get_loss(self):
        raise NotImplementedError()

    def get_per_sample_loss(self):
        raise NotImplementedError()

    def torch(self):
        raise NotImplementedError()

    def get_inputs(self):
        return self.inputs

    def get_labels(self):
        raise NotImplementedError()

    def get_dataset(self):
        raise NotImplementedError()

    def get_metrics(self):
        for i in range(len(self.metrics)):
            metric_name, metric = self.metrics[i]
            metric.bind_to_task(self)
        return self.metrics

    def __repr__(self):
        params = (
            ('name', self.get_name()),
            ('module', self.torch()),
            ('loss', self.get_loss()),
            ('activation', self.get_activation()),
            ('decoder', self.get_decoder()),
            ('available_func', self.get_available_func()),
            ('per_sample_loss', self.get_per_sample_loss())
        )
        params_str = os.linesep.join(map(lambda x: f'\t{x[0]}={x[1]}', params))
        params_str = f'{os.linesep}{params_str}{os.linesep}'
        res = f'{self.__class__.__module__}.{self.__class__.__name__}({params_str}) at {hex(id(self))}'
        return res


@dataclass
class Task(ITask):
    name: str
    labels: Any
    loss: nn.Module
    per_sample_loss: nn.Module
    available_func: Callable
    inputs: Any
    activation: Optional[nn.Module]
    decoder: Decoder
    module: nn.Module
    metrics: Tuple[str, TorchMetric]

    def get_activation(self) -> Optional[nn.Module]:
        return self.activation

    def get_decoder(self):
        return self.decoder

    def get_loss(self):
        return self.loss

    def get_per_sample_loss(self):
        return self.per_sample_loss

    def torch(self):
        return self.module

    def get_inputs(self, *args, **kwargs):
        return self.inputs

    def get_labels(self, *args, **kwargs):
        return self.labels

    def get_dataset(self, **kwargs):
        return LeafTaskDataset(self.inputs, self.labels)


@dataclass()
class BinaryHardcodedTask(Task):
    name: str
    labels: Any
    loss: nn.Module = None
    per_sample_loss: nn.Module = None
    available_func: Callable = positive_values
    inputs: Any = None
    activation: Optional[nn.Module] = None
    decoder: Decoder = None
    module: nn.Module = Identity()
    metrics: Tuple[str, TorchMetric] = ()


@dataclass()
class BoundedRegressionTask(Task):
    """
    Represents a regression task, where the labels are normalized between 0 and 1. Examples include bounding box top
    left corners regression. Here are the defaults:
    * activation - `nn.Sigmoid()` - so that the output is in `[0, 1]`
    * loss - `SigmoidAndMSELoss` - sigmoid on the logits, then standard mean squared error loss.
    """
    name: str
    labels: Any
    loss: nn.Module = field(default_factory=lambda: SigmoidAndMSELoss(reduction='mean'))
    per_sample_loss: nn.Module = field(default_factory=lambda: ReducedPerSample(SigmoidAndMSELoss(reduction='none'), reduction=torch.sum))
    available_func: Callable = field(default_factory=lambda: positive_values)
    module: nn.Module = field(default_factory=lambda: nn.Identity())
    activation: nn.Module = field(default_factory=lambda: nn.Sigmoid())
    decoder: Decoder = None
    inputs: Any = None
    metrics: Tuple = field(default_factory=get_default_bounded_regression_metrics)


@dataclass()
class BinaryClassificationTask(Task):
    """
    Represents a normal binary classification task. Labels should be between 0 and 1.
    * activation - `nn.Sigmoid()`
    * loss - ``nn.BCEWithLogitsLoss()`
    """
    name: str
    labels: Any
    loss: nn.Module = nn.BCEWithLogitsLoss(reduction='mean')
    per_sample_loss: nn.Module = ReducedPerSample(nn.BCEWithLogitsLoss(reduction='none'), reduction=torch.mean)
    available_func: Callable = positive_values
    inputs: Any = None
    activation: Optional[nn.Module] = nn.Sigmoid()
    decoder: Decoder = field(default_factory=BinaryDecoder)
    module: nn.Module = Identity()
    metrics: Tuple[str, TorchMetric] = field(default_factory=get_default_binary_metrics)


@dataclass
class ClassificationTask(Task):
    """
    Represents a classification task. Labels should be integers from 0 to N-1, where N is the number of classes
    * activation - `nn.Softmax(dim=-1)`
    * loss - `nn.CrossEntropyLoss()`
    """
    name: str
    labels: Any
    loss: nn.Module = nn.CrossEntropyLoss(reduction='mean')
    per_sample_loss: nn.Module = ReducedPerSample(nn.CrossEntropyLoss(reduction='none'), torch.mean)
    available_func: Callable = positive_values_unsqueezed
    inputs: Any = None
    activation: Optional[nn.Module] = nn.Sigmoid()
    decoder: Decoder = field(default_factory=ClassificationDecoder)
    module: nn.Module = Identity()
    metrics: Tuple[str, TorchMetric] = field(default_factory=get_default_classification_metrics)


@dataclass()
class MultilabelClassificationTask(Task):
    """
    Represents a classification task. Labels should be integers from 0 to N-1, where N is the number of classes
    * activation - `nn.Softmax(dim=-1)`
    * loss - `nn.CrossEntropyLoss()`
    """
    name: str
    labels: Any
    loss: nn.Module = nn.BCEWithLogitsLoss(reduction='mean')
    per_sample_loss: nn.Module = ReducedPerSample(nn.BCEWithLogitsLoss(reduction='none'), torch.mean)
    available_func: Callable = has_no_missing_labels
    inputs: Any = None
    activation: Optional[nn.Module] = nn.Sigmoid()
    decoder: Decoder = field(default_factory=MultilabelClassificationDecoder)
    module: nn.Module = Identity()
    metrics: Tuple[str, TorchMetric] = field(default_factory=get_default_multilabel_classification_metrics)


class TaskFlow(ITask):

    def __init__(self, name, tasks: Iterable[ITask], flow_func=None, inputs=None, available_func=None):
        super().__init__(name, inputs, available_func)
        self.tasks = {}
        for task in tasks:
            self.tasks[task.get_name()] = task
        if flow_func is not None:
            self._flow_func = flow_func

    def get_loss(self):
        return TaskFlowLoss(self, parent_reduction='mean', child_reduction='per_sample')

    def get_per_sample_loss(self):
        return TaskFlowLoss(self, parent_reduction='per_sample', child_reduction='per_sample')

    def torch(self):
        return TaskFlowModule(self)

    def has_children(self):
        return True

    def get_dataset(self, **kwargs) -> Dataset:
        return FlowDataset(self, **kwargs)

    def flow(self, x, out):
        raise NotImplementedError()

    def get_flow_func(self):
        if hasattr(self, '_flow_func') and self._flow_func is not None:
            return self._flow_func
        return self.__class__.flow

    def get_metrics(self):
        all_metrics = []
        for task in self.tasks.values():
            all_metrics += task.get_metrics()
        return all_metrics

    def get_treelib_explainer(self):
        return TreeExplainer(self)

    def get_labels(self, *args, **kwargs):
        all_labels = []
        for task in self.tasks.values():
            all_labels += task.get_labels()
        return all_labels

    def get_decoder(self):
        return TaskFlowDecoder(self)

    def get_activation(self) -> Optional[nn.Module]:
        return CompositeActivation(self)

    def get_evaluator(self):
        return EvaluationCompositeVisitor(self, prefix='')

    def get_filter(self):
        return FilterCompositeVisitor(self, prefix='')

    def get_all_children(self, prefix=''):
        tasks = {}
        for task_name, task in self.tasks.items():
            if task.has_children():
                tasks.update(task.get_all_children(prefix=f'{prefix}{task.get_name()}.'))
            else:
                tasks[prefix + task_name] = task
        return tasks

