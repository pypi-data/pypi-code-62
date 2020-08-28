# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: train.py
@time: 2019/12/27 14:41

这一行开始写关于本文件的说明与解释


"""
import argparse
import logging
import os
from typing import Any, Dict, List, Optional

from overrides import overrides

from leslie.commands.subcommand import Subcommand
from leslie.common import Params, Registrable, Lazy
from leslie.common.checks import ConfigurationError
from leslie.common.logging import prepare_global_logging
from leslie.common import util as common_util
from leslie.data import DatasetReader, Vocabulary
from leslie.models.archival import archive_model, CONFIG_NAME
from leslie.models.model import Model
from leslie.training.trainer import Trainer
from leslie.training import util as training_util

logger = logging.getLogger(__name__)


@Subcommand.register("train")
class Train(Subcommand):
    @overrides
    def add_subparser(self, parser: argparse._SubParsersAction) -> argparse.ArgumentParser:
        description = """Train the specified model on the specified dataset."""
        subparser = parser.add_parser(self.name, description=description, help="Train a model.")

        subparser.add_argument(
            "param_path", type=str, help="path to parameter file describing the model to be trained"
        )

        subparser.add_argument(
            "-s",
            "--serialization-dir",
            required=True,
            type=str,
            help="directory in which to save the model and its logs",
        )

        subparser.add_argument(
            "-r",
            "--recover",
            action="store_true",
            default=False,
            help="recover training from the state in serialization_dir",
        )

        subparser.add_argument(
            "-f",
            "--force",
            action="store_true",
            required=False,
            help="overwrite the output directory if it exists",
        )

        subparser.add_argument(
            "-o",
            "--overrides",
            type=str,
            default="",
            help="a JSON structure used to override the experiment configuration",
        )

        subparser.add_argument(
            "--file-friendly-logging",
            action="store_true",
            default=False,
            help="outputs tqdm status on separate lines and slows tqdm refresh rate",
        )

        subparser.add_argument(
            "--node-rank", type=int, default=0, help="rank of this node in the distributed setup"
        )

        subparser.add_argument(
            "--dry-run",
            action="store_true",
            help="do not train a model, but create a vocabulary, show dataset statistics and "
                 "other training information",
        )

        subparser.set_defaults(func=train_model_from_args)

        return subparser


def train_model_from_args(args: argparse.Namespace):
    """
    Just converts from an `argparse.Namespace` object to string paths.
    """
    train_model_from_file(
        parameter_filename=args.param_path,
        serialization_dir=args.serialization_dir,
        overrides=args.overrides,
        file_friendly_logging=args.file_friendly_logging,
        recover=args.recover,
        force=args.force,
        node_rank=args.node_rank,
        include_package=args.include_package,
        dry_run=args.dry_run,
    )


def train_model_from_file(
        parameter_filename: str,
        serialization_dir: str,
        overrides: str = "",
        file_friendly_logging: bool = False,
        recover: bool = False,
        force: bool = False,
        node_rank: int = 0,
        include_package: List[str] = None,
        dry_run: bool = False,
) -> Optional[Model]:
    """
    A wrapper around [`train_model`](#train_model) which loads the params from a file.

    # Parameters

    parameter_filename : `str`
        A json parameter file specifying an AllenNLP experiment.
    serialization_dir : `str`
        The directory in which to save results and logs. We just pass this along to
        [`train_model`](#train_model).
    overrides : `str`
        A JSON string that we will use to override values in the input parameter file.
    file_friendly_logging : `bool`, optional (default=False)
        If `True`, we make our output more friendly to saved model files.  We just pass this
        along to [`train_model`](#train_model).
    recover : `bool`, optional (default=False)
        If `True`, we will try to recover a training run from an existing serialization
        directory.  This is only intended for use when something actually crashed during the middle
        of a run.  For continuing training a model on new data, see `Model.from_archive`.
    force : `bool`, optional (default=False)
        If `True`, we will overwrite the serialization directory if it already exists.
    node_rank : `int`, optional
        Rank of the current node in distributed training
    include_package : `str`, optional
        In distributed mode, extra packages mentioned will be imported in trainer workers.
    dry_run : `bool`, optional (default=False)
        Do not train a model, but create a vocabulary, show dataset statistics and other training
        information.

    # Returns

    best_model : `Optional[Model]`
        The model with the best epoch weights or `None` if in dry run.
    """
    # Load the experiment config from a file and pass it to `train_model`.
    params = Params.from_file(parameter_filename, overrides)
    return train_model(
        params=params,
        serialization_dir=serialization_dir,
        file_friendly_logging=file_friendly_logging,
        recover=recover,
        force=force,
        node_rank=node_rank,
        include_package=include_package,
        dry_run=dry_run,
    )


def train_model(
        params: Params,
        serialization_dir: str,
        file_friendly_logging: bool = False,
        recover: bool = False,
        force: bool = False,
        node_rank: int = 0,
        include_package: List[str] = None,
        batch_weight_key: str = "",
        dry_run: bool = False,
) -> Optional[Model]:
    """
    Trains the model specified in the given [`Params`](../common/params.md#params) object, using the data
    and training parameters also specified in that object, and saves the results in `serialization_dir`.

    # Parameters

    params : `Params`
        A parameter object specifying an AllenNLP Experiment.
    serialization_dir : `str`
        The directory in which to save results and logs.
    file_friendly_logging : `bool`, optional (default=False)
        If `True`, we add newlines to tqdm output, even on an interactive terminal, and we slow
        down tqdm's output to only once every 10 seconds.
    recover : `bool`, optional (default=False)
        If `True`, we will try to recover a training run from an existing serialization
        directory.  This is only intended for use when something actually crashed during the middle
        of a run.  For continuing training a model on new data, see `Model.from_archive`.
    force : `bool`, optional (default=False)
        If `True`, we will overwrite the serialization directory if it already exists.
    node_rank : `int`, optional
        Rank of the current node in distributed training
    include_package : `List[str]`, optional
        In distributed mode, extra packages mentioned will be imported in trainer workers.
    batch_weight_key : `str`, optional (default="")
        If non-empty, name of metric used to weight the loss on a per-batch basis.
    dry_run : `bool`, optional (default=False)
        Do not train a model, but create a vocabulary, show dataset statistics and other training
        information.

    # Returns

    best_model : `Optional[Model]`
        The model with the best epoch weights or `None` if in dry run.
    """
    training_util.create_serialization_dir(params, serialization_dir, recover, force)
    params.to_file(os.path.join(serialization_dir, CONFIG_NAME))

    # one cuda device, we just run a single training process.
    model = _train_worker(
        process_rank=0,
        params=params,
        serialization_dir=serialization_dir,
        file_friendly_logging=file_friendly_logging,
        include_package=include_package,
        batch_weight_key=batch_weight_key,
        dry_run=dry_run,
    )
    if not dry_run:
        archive_model(serialization_dir)
    return model


def _train_worker(
        process_rank: int,
        params: Params,
        serialization_dir: str,
        file_friendly_logging: bool = False,
        batch_weight_key: str = "",
        dry_run: bool = False,
        world_size: int = 1,
) -> Optional[Model]:
    """
    Helper to train the configured model/experiment.. In a single GPU experiment, this returns the `Model` object and
    # Parameters

    process_rank : `int`
        The process index that is initialized using the GPU device id.
    params : `Params`
        A parameter object specifying an AllenNLP Experiment.
    serialization_dir : `str`
        The directory in which to save results and logs.
    file_friendly_logging : `bool`, optional (default=False)
        If `True`, we add newlines to tqdm output, even on an interactive terminal, and we slow
        down tqdm's output to only once every 10 seconds.
    include_package : `List[str]`, optional
        In distributed mode, since this function would have been spawned as a separate process,
        the extra imports need to be done again. NOTE: This does not have any effect in single
        GPU training.
    batch_weight_key : `str`, optional (default="")
        If non-empty, name of metric used to weight the loss on a per-batch basis.
    dry_run : `bool`, optional (default=False)
        Do not train a model, but create a vocabulary, show dataset statistics and other training
        information.
    world_size : `int`, optional
        The number of processes involved in distributed training.

    # Returns

    best_model : `Optional[Model]`
        The model with the best epoch weights or `None` if in distributed training or in dry run.
    """
    prepare_global_logging(
        serialization_dir, file_friendly_logging, rank=process_rank, world_size=world_size
    )
    common_util.prepare_environment(params)
    train_loop = TrainModel.from_params(
        params=params,
        serialization_dir=serialization_dir,
        local_rank=process_rank,
        batch_weight_key=batch_weight_key,
    )

    if dry_run:
        return None
    metrics = train_loop.run()
    train_loop.finish(metrics)
    return train_loop.model


class TrainModel(Registrable):
    """
    This class exists so that we can easily read a configuration file with the `allennlp train`
    command.  The basic logic is that we call `train_loop =
    TrainModel.from_params(params_from_config_file)`, then `train_loop.run()`.  This class performs
    very little logic, pushing most of it to the `Trainer` that has a `train()` method.  The
    point here is to construct all of the dependencies for the `Trainer` in a way that we can do
    it using `from_params()`, while having all of those dependencies transparently documented and
    not hidden in calls to `params.pop()`.  If you are writing your own training loop, you almost
    certainly should not use this class, but you might look at the code for this class to see what
    we do, to make writing your training loop easier.

    In particular, if you are tempted to call the `__init__` method of this class, you are probably
    doing something unnecessary.  Literally all we do after `__init__` is call `trainer.train()`.  You
    can do that yourself, if you've constructed a `Trainer` already.  What this class gives you is a
    way to construct the `Trainer` by means of a config file.  The actual constructor that we use
    with `from_params` in this class is `from_partial_objects`.  See that method for a description
    of all of the allowed top-level keys in a configuration file used with `leslie train`.
    """

    default_implementation = "default"
    """
    The default implementation is registered as 'default'.
    """

    def __init__(
            self,
            serialization_dir: str,
            model: Model,
            trainer: Trainer,
            evaluation_data_loader=None,
            evaluate_on_test: bool = False,
            batch_weight_key: str = "",
    ) -> None:
        self.serialization_dir = serialization_dir
        self.model = model
        self.trainer = trainer
        self.evaluation_data_loader = evaluation_data_loader
        self.evaluate_on_test = evaluate_on_test
        self.batch_weight_key = batch_weight_key

    def run(self) -> Dict[str, Any]:
        return self.trainer.train()

    def finish(self, metrics: Dict[str, Any]):
        if self.evaluation_data_loader and self.evaluate_on_test:
            logger.info("The model will be evaluated using the best epoch weights.")
            test_metrics = training_util.evaluate(
                self.model,
                self.evaluation_data_loader,
                cuda_device=self.trainer.cuda_device,
                batch_weight_key=self.batch_weight_key,
            )

            for key, value in test_metrics.items():
                metrics["test_" + key] = value
        elif self.evaluation_data_loader:
            logger.info(
                "To evaluate on the test set after training, pass the "
                "'evaluate_on_test' flag, or use the 'allennlp evaluate' command."
            )
        common_util.dump_metrics(
            os.path.join(self.serialization_dir, "metrics.json"), metrics, log=True
        )

    @classmethod
    def from_partial_objects(
            cls,
            serialization_dir: str,
            local_rank: int,
            batch_weight_key: str,
            dataset_reader: DatasetReader,
            train_data_path: str,
            model: Lazy[Model],
            trainer: Lazy[Trainer],
            data_loader=None,
            vocabulary: Lazy[Vocabulary] = None,
            datasets_for_vocab_creation: List[str] = None,
            validation_dataset_reader: DatasetReader = None,
            validation_data_path: str = None,
            validation_data_loader=None,
            test_data_path: str = None,
            evaluate_on_test: bool = False,
    ) -> "TrainModel":
        """
        This method is intended for use with our `FromParams` logic, to construct a `TrainModel`
        object from a config file passed to the `allennlp train` command.  The arguments to this
        method are the allowed top-level keys in a configuration file (except for the first three,
        which are obtained separately).

        You *could* use this outside of our `FromParams` logic if you really want to, but there
        might be easier ways to accomplish your goal than instantiating `Lazy` objects.  If you are
        writing your own training loop, we recommend that you look at the implementation of this
        method for inspiration and possibly some utility functions you can call, but you very likely
        should not use this method directly.

        The `Lazy` type annotations here are a mechanism for building dependencies to an object
        sequentially - the `TrainModel` object needs data, a model, and a trainer, but the model
        needs to see the data before it's constructed (to create a vocabulary) and the trainer needs
        the data and the model before it's constructed.  Objects that have sequential dependencies
        like this are labeled as `Lazy` in their type annotations, and we pass the missing
        dependencies when we call their `construct()` method, which you can see in the code below.

        # Parameters
        serialization_dir: `str`
            The directory where logs and model archives will be saved.
        local_rank: `int`
            The process index that is initialized using the GPU device id.
        batch_weight_key: `str`
            The name of metric used to weight the loss on a per-batch basis.
        dataset_reader: `DatasetReader`
            The `DatasetReader` that will be used for training and (by default) for validation.
        train_data_path: `str`
            The file (or directory) that will be passed to `dataset_reader.read()` to construct the
            training data.
        model: `Lazy[Model]`
            The model that we will train.  This is lazy because it depends on the `Vocabulary`;
            after constructing the vocabulary we call `model.construct(vocab=vocabulary)`.
        data_loader: `Lazy[DataLoader]`
            The data_loader we use to batch instances from the dataset reader at training and (by
            default) validation time. This is lazy because it takes a dataset in it's constructor.
        trainer: `Lazy[Trainer]`
            The `Trainer` that actually implements the training loop.  This is a lazy object because
            it depends on the model that's going to be trained.
        vocabulary: `Lazy[Vocabulary]`, optional (default=None)
            The `Vocabulary` that we will use to convert strings in the data to integer ids (and
            possibly set sizes of embedding matrices in the `Model`).  By default we construct the
            vocabulary from the instances that we read.
        datasets_for_vocab_creation: `List[str]`, optional (default=None)
            If you pass in more than one dataset but don't want to use all of them to construct a
            vocabulary, you can pass in this key to limit it.  Valid entries in the list are
            "train", "validation" and "test".
        validation_dataset_reader: `DatasetReader`, optional (default=None)
            If given, we will use this dataset reader for the validation data instead of
            `dataset_reader`.
        validation_data_path: `str`, optional (default=None)
            If given, we will use this data for computing validation metrics and early stopping.
        validation_data_loader: `Lazy[DataLoader]`, optional (default=None)
            If given, the data_loader we use to batch instances from the dataset reader at
            validation and test time. This is lazy because it takes a dataset in it's constructor.
        test_data_path: `str`, optional (default=None)
            If given, we will use this as test data.  This makes it available for vocab creation by
            default, but nothing else.
        evaluate_on_test: `bool`, optional (default=False)
            If given, we will evaluate the final model on this data at the end of training.  Note
            that we do not recommend using this for actual test data in every-day experimentation;
            you should only very rarely evaluate your model on actual test data.
        """

        datasets = training_util.read_all_datasets(
            train_data_path=train_data_path,
            dataset_reader=dataset_reader,
            validation_dataset_reader=validation_dataset_reader,
            validation_data_path=validation_data_path,
            test_data_path=test_data_path,
        )

        if datasets_for_vocab_creation:
            for key in datasets_for_vocab_creation:
                if key not in datasets:
                    raise ConfigurationError(f"invalid 'dataset_for_vocab_creation' {key}")

        instance_generator = (
            instance
            for key, dataset in datasets.items()
            if not datasets_for_vocab_creation or key in datasets_for_vocab_creation
            for instance in dataset
        )

        vocabulary_ = vocabulary.construct(instances=instance_generator)
        if not vocabulary_:
            vocabulary_ = Vocabulary.from_instances(instance_generator)
        model_ = model.construct(vocab=vocabulary_)

        # Initializing the model can have side effect of expanding the vocabulary.
        # Save the vocab only in the master. In the degenerate non-distributed
        # case, we're trivially the master.
        if common_util.is_master():
            vocabulary_path = os.path.join(serialization_dir, "vocabulary")
            vocabulary_.save_to_files(vocabulary_path)

        for dataset in datasets.values():
            dataset.index_with(model_.vocab)

        data_loader_ = data_loader.construct(dataset=datasets["train"])
        validation_data = datasets.get("validation")
        if validation_data is not None:
            # Because of the way Lazy[T] works, we can't check it's existence
            # _before_ we've tried to construct it. It returns None if it is not
            # present, so we try to construct it first, and then afterward back off
            # to the data_loader configuration used for training if it returns None.
            validation_data_loader_ = validation_data_loader.construct(dataset=validation_data)
            if validation_data_loader_ is None:
                validation_data_loader_ = data_loader.construct(dataset=validation_data)
        else:
            validation_data_loader_ = None

        test_data = datasets.get("test")
        if test_data is not None:
            test_data_loader = validation_data_loader.construct(dataset=test_data)
            if test_data_loader is None:
                test_data_loader = data_loader.construct(dataset=test_data)
        else:
            test_data_loader = None

        # We don't need to pass serialization_dir and local_rank here, because they will have been
        # passed through the trainer by from_params already, because they were keyword arguments to
        # construct this class in the first place.
        trainer_ = trainer.construct(
            model=model_, data_loader=data_loader_, validation_data_loader=validation_data_loader_,
        )

        return cls(
            serialization_dir=serialization_dir,
            model=model_,
            trainer=trainer_,
            evaluation_data_loader=test_data_loader,
            evaluate_on_test=evaluate_on_test,
            batch_weight_key=batch_weight_key,
        )


TrainModel.register("default", constructor="from_partial_objects")(TrainModel)
