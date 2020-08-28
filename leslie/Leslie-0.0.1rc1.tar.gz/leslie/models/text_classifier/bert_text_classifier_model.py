# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: bert_text_classifier.py
@time: 2019/12/10 14:31

这一行开始写关于本文件的说明与解释


"""

import codecs
import csv
import pickle

import tensorflow as tf
import collections
from bakend.bert import tokenization
from bakend.bert import modeling, optimization
import os

tf.logging.set_verbosity(tf.logging.INFO)


# os.environ['CUDA_VISIBLE_DEVICES'] = '1'

class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_test_examples(self, data_dir):
        """Gets a collection of `InputExample`s for prediction."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with tf.gfile.Open(input_file, "r") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                lines.append(line)
            return lines


class MyProcessor(DataProcessor):
    def __init__(self):
        super(MyProcessor).__init__()

    def get_train_examples(self, data_dir):
        with open(os.path.join(data_dir, "train.txt"), "r", encoding="utf-8") as f:
            lines = []
            for line in f:
                lines.append(line.replace("\n", "").strip())
        return self._create_examples(lines, "train")

    def get_dev_examples(self, data_dir):
        with open(os.path.join(data_dir, "eval.txt"), "r", encoding="utf-8") as f:
            lines = []
            for line in f:
                lines.append(line.replace("\n", "").strip())
        return self._create_examples(lines, "eval")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            # Only the test set has a header
            if set_type == "test" and i == 0:
                continue
            guid = "%s-%s" % (set_type, i)
            if set_type == "test":
                text_a = tokenization.convert_to_unicode(line[1])
                label = "0"
            else:
                text_a = tokenization.convert_to_unicode(line[0:-1].strip())
                label = tokenization.convert_to_unicode(line[-1].strip())
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
        return examples


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.

        Args:
          guid: Unique id for the example.
          text_a: string. The untokenized leslie of the first sequence. For single
            sequence tasks, only this sequence must be specified.
          text_b: (Optional) string. The untokenized leslie of the second sequence.
            Only must be specified for sequence pair tasks.
          label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self,
                 input_ids,
                 input_mask,
                 segment_ids,
                 label_id,
                 is_real_example=True):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.is_real_example = is_real_example


class BertClassifier:
    def __init__(self):
        self.data_root = './pretrained/chinese_L-12_H-768_A-12/'
        self.bert_config_file = self.data_root + 'bert_config.json'
        self.init_checkpoint = self.data_root + 'bert_model.ckpt'
        self.bert_vocab_file = self.data_root + 'vocab.txt'
        self.bert_config = modeling.BertConfig.from_json_file(self.bert_config_file)
        self.tokenizer = tokenization.FullTokenizer(vocab_file=self.bert_vocab_file)
        self.output_dir = ''

    def conver_single_example(self, ex_index, example, label_list, max_seq_length, tokenizer, mode):
        """
        将一个训练样本转化为InputFeature，其中进行字符seg并且index化,和label的index转化
        :param ex_index:
        :param example:
        :param label_list:
        :param max_seq_length:
        :param tokenizer:
        :return:
        """
        # 1. 构建label->id的映射
        label_map = {}
        if os.path.exists(os.path.join(self.output_dir, 'label2id.pkl')):
            with codecs.open(os.path.join(self.output_dir, 'label2id.pkl'), 'rb') as fd:
                label_map = pickle.load(fd)
        else:
            for i, label in enumerate(label_list):
                label_map[label] = i
            with codecs.open(os.path.join(self.output_dir, 'label2id.pkl'), 'wb') as fd:
                pickle.dump(label_map, fd)
        # 不考虑seq pair 分类的情况
        tokens_a = tokenizer.tokenize(example.text_a)

        # 截断，因为有句首和句尾的标识符
        if len(tokens_a) > max_seq_length - 2:
            tokens_a = tokens_a[0:(max_seq_length - 2)]

        tokens = []
        segment_ids = []
        tokens.append('[CLS]')
        segment_ids.append(0)
        for token in tokens_a:
            tokens.append(token)
            segment_ids.append(0)
        tokens.append('[SEP]')
        segment_ids.append(0)
        # 将字符转化为id形式
        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        input_mask = [1] * len(input_ids)
        # 补全到max_seg_length
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            segment_ids.append(0)
            input_mask.append(0)
        if example.label is None:
            label_id = -1
        else:
            label_id = label_map[example.label]
        if ex_index < 2 and mode in ['train', 'dev']:
            tf.logging.info("*** Example ***")
            tf.logging.info("guid: %s" % (example.guid))
            tf.logging.info("tokens: %s" % " ".join(
                [tokenization.printable_text(x) for x in tokens]))
            tf.logging.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            tf.logging.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            tf.logging.info("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
            tf.logging.info("label: %s (id = %d)" % (example.label, label_id))

        feature = InputFeatures(input_ids=input_ids, input_mask=input_mask, segment_ids=segment_ids, label_id=label_id)
        return feature

    def file_based_convert_examples_to_features(self, examples, label_list, max_seq_length, tokenizer, output_file,
                                                mode):
        """
        将训练文件转化特征后，存储为tf_record格式，用于模型的读取
        :param mode:
        :param examples:
        :param label_list:
        :param max_seq_length:
        :param tokenizer:
        :param output_file:
        :return:
        """
        writer = tf.python_io.TFRecordWriter(path=output_file)
        # 将每一个样本转化为idx特征，封装到map中后进行序列化存储为record
        for ex_index, example in enumerate(examples):
            if ex_index % 10000 == 0:
                tf.logging.info("Writing example %d of %d" % (ex_index, len(examples)))
            feature = self.conver_single_example(ex_index, example, label_list, max_seq_length, tokenizer, mode)

            # 将输入数据转化为64位int 的list，这是必须的
            def create_int_feature(values):
                f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
                return f

            features = collections.OrderedDict()
            features['input_ids'] = create_int_feature(feature.input_ids)
            features['input_mask'] = create_int_feature(feature.input_mask)
            features['segment_ids'] = create_int_feature(feature.segment_ids)
            features['label_ids'] = create_int_feature([feature.label_id])
            features["is_real_example"] = create_int_feature(
                [int(feature.is_real_example)])
            # 转化为Example 协议内存块
            tf_example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(tf_example.SerializeToString())

    def file_based_input_fn_builder(self, input_file, seq_length, is_training,
                                    drop_remainder):
        """Creates an `input_fn` closure to be passed to TPUEstimator."""

        name_to_features = {
            "input_ids": tf.FixedLenFeature([seq_length], tf.int64),
            "input_mask": tf.FixedLenFeature([seq_length], tf.int64),
            "segment_ids": tf.FixedLenFeature([seq_length], tf.int64),
            "label_ids": tf.FixedLenFeature([], tf.int64),
            "is_real_example": tf.FixedLenFeature([], tf.int64),
        }

        def _decode_record(record, name_to_features):
            """Decodes a record to a TensorFlow example."""
            example = tf.parse_single_example(record, name_to_features)

            # tf.Example only supports tf.int64, but the TPU only supports tf.int32.
            # So cast all int64 to int32.
            for name in list(example.keys()):
                t = example[name]
                if t.dtype == tf.int64:
                    t = tf.to_int32(t)
                example[name] = t

            return example

        def input_fn(params):
            """The actual input function."""
            batch_size = params["batch_size"]

            # For training, we want a lot of parallel reading and shuffling.
            # For eval, we want no shuffling and parallel reading doesn't matter.
            d = tf.data.TFRecordDataset(input_file)
            if is_training:
                d = d.repeat()
                d = d.shuffle(buffer_size=100)

            d = d.apply(
                tf.contrib.data.map_and_batch(
                    lambda record: _decode_record(record, name_to_features),
                    batch_size=batch_size,
                    drop_remainder=drop_remainder))

            return d

        return input_fn

    def create_model(self, is_training, input_ids, input_mask, segment_ids,
                     labels, num_labels):
        """Creates a classification model."""
        model = modeling.BertModel(
            config=self.bert_config,
            is_training=is_training,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=segment_ids)

        output_layer = model.get_pooled_output()

        hidden_size = output_layer.shape[-1].value

        output_weights = tf.get_variable(
            "output_weights", [num_labels, hidden_size],
            initializer=tf.truncated_normal_initializer(stddev=0.02))

        output_bias = tf.get_variable(
            "output_bias", [num_labels], initializer=tf.zeros_initializer())

        with tf.variable_scope("loss"):
            if is_training:
                # I.e., 0.1 dropout
                output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)

            logits = tf.matmul(output_layer, output_weights, transpose_b=True)
            logits = tf.nn.bias_add(logits, output_bias)
            probabilities = tf.nn.softmax(logits, axis=-1)
            log_probs = tf.nn.log_softmax(logits, axis=-1)

            one_hot_labels = tf.one_hot(labels, depth=num_labels, dtype=tf.float32)

            per_example_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
            loss = tf.reduce_mean(per_example_loss)

            return loss, per_example_loss, logits, probabilities

    def model_fn_builder(self, num_labels, init_checkpoint, learning_rate,
                         num_train_steps, num_warmup_steps):

        def model_fn(features, labels, mode, params):  # pylint: disable=unused-argument
            """The `model_fn` for TPUEstimator."""

            tf.logging.info("*** Features ***")
            for name in sorted(features.keys()):
                tf.logging.info("  name = %s, shape = %s" % (name, features[name].shape))

            input_ids = features["input_ids"]
            input_mask = features["input_mask"]
            segment_ids = features["segment_ids"]
            label_ids = features["label_ids"]
            if "is_real_example" in features:
                is_real_example = tf.cast(features["is_real_example"], dtype=tf.float32)
            else:
                is_real_example = tf.ones(tf.shape(label_ids), dtype=tf.float32)

            is_training = (mode == tf.estimator.ModeKeys.TRAIN)

            total_loss, per_example_loss, logits, probabilities = self.create_model(
                is_training, input_ids, input_mask, segment_ids, label_ids,
                num_labels)

            tvars = tf.trainable_variables()
            initialized_variable_names = {}
            if init_checkpoint:
                assignment_map, initialized_variable_names = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                         init_checkpoint)
                tf.train.init_from_checkpoint(init_checkpoint, assignment_map)
            tf.logging.info("**** Trainable Variables ****")
            for var in tvars:
                init_string = ""
                if var.name in initialized_variable_names:
                    init_string = ", *INIT_FROM_CKPT*"
                tf.logging.info("  name = %s, shape = %s%s", var.name, var.shape,
                                init_string)
            output_spec = None
            if mode == tf.estimator.ModeKeys.TRAIN:
                train_op = optimization.create_optimizer(
                    total_loss, learning_rate, num_train_steps, num_warmup_steps, use_tpu=False)

                output_spec = tf.estimator.EstimatorSpec(
                    mode=mode,
                    loss=total_loss,
                    train_op=train_op)
            elif mode == tf.estimator.ModeKeys.EVAL:
                def metric_fn(per_example_loss, label_ids, logits, is_real_example):
                    predictions = tf.argmax(logits, axis=-1, output_type=tf.int32)
                    accuracy = tf.metrics.accuracy(
                        labels=label_ids, predictions=predictions, weights=is_real_example)
                    loss = tf.metrics.mean(values=per_example_loss, weights=is_real_example)
                    return {
                        "eval_accuracy": accuracy,
                        "eval_loss": loss,
                    }

                eval_metrics = metric_fn(per_example_loss, label_ids, logits, is_real_example)
                output_spec = tf.estimator.EstimatorSpec(
                    mode=mode,
                    loss=total_loss,
                    eval_metric_ops=eval_metrics)
            else:
                raise ValueError("mod should be one of `train`, `dev`.")
            return output_spec

        return model_fn

    def run(self, output_dir, save_summary_steps, save_checkpoints_steps, data_dir, train_batch_size, learning_rate,
            num_train_epochs, warmup_proportion, max_seq_length, mod, eval_batch_size=4):
        self.output_dir = output_dir
        tf.gfile.MakeDirs(output_dir)
        run_config = tf.estimator.RunConfig(
            model_dir=output_dir,
            save_summary_steps=save_summary_steps,
            save_checkpoints_steps=save_checkpoints_steps,
            keep_checkpoint_max=5,
            log_step_count_steps=32,
            session_config=tf.ConfigProto(log_device_placement=True)
            # session_config=tf.ConfigProto(log_device_placement=True,
            #                               device_count={'GPU': 1}))
        )
        data_processor = MyProcessor()
        label_list = data_processor.get_labels()
        tf.logging.info('************ label_list=' + ' '.join(label_list))
        if mod == "train":
            train_examples = data_processor.get_train_examples(data_dir=data_dir)
            num_train_steps = int(
                len(train_examples) / train_batch_size * num_train_epochs)
            num_warmup_steps = int(num_train_steps * warmup_proportion)
        elif mod == "dev":
            train_examples = None
            num_train_steps = None
            num_warmup_steps = None
        else:
            raise ValueError("mod must be one of `train`, `dev`.")
        model_fn = self.model_fn_builder(
            num_labels=len(label_list),
            init_checkpoint=self.init_checkpoint,
            learning_rate=learning_rate,
            num_train_steps=num_train_steps,
            num_warmup_steps=num_warmup_steps
        )
        params = {
            'batch_size': train_batch_size,
        }
        estimator = tf.estimator.Estimator(
            model_fn=model_fn,
            config=run_config,
            params=params,
        )
        if mod == "train":
            self.train(output_dir, train_examples, label_list, max_seq_length, train_batch_size, num_train_steps,
                       estimator)
        elif mod == "dev":
            eval_examples = data_processor.get_dev_examples(data_dir=data_dir)
            self.eval(output_dir, eval_examples, label_list, max_seq_length, eval_batch_size, estimator)
        else:
            raise ValueError("mod should be one of `train`, `dev`.")

    def train(self, output_dir, train_examples, label_list, max_seq_length, train_batch_size, num_train_steps,
              estimator,
              ):
        train_file = os.path.join(output_dir, "train.tf_record")
        self.file_based_convert_examples_to_features(
            train_examples, label_list, max_seq_length, self.tokenizer, train_file, 'train')
        tf.logging.info("***** Running training *****")
        tf.logging.info("  Num examples = %d", len(train_examples))
        tf.logging.info("  Batch size = %d", train_batch_size)
        tf.logging.info("  Num steps = %d", num_train_steps)
        train_input_fn = self.file_based_input_fn_builder(
            input_file=train_file,
            seq_length=max_seq_length,
            is_training=True,
            drop_remainder=True)
        estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)

    def eval(self, output_dir, eval_examples, label_list, max_seq_length, eval_batch_size, estimator):
        num_actual_eval_examples = len(eval_examples)
        eval_file = os.path.join(output_dir, "eval.tf_record")
        self.file_based_convert_examples_to_features(
            eval_examples, label_list, max_seq_length, self.tokenizer, eval_file, mode='dev')
        tf.logging.info("***** Running evaluation *****")
        tf.logging.info("  Num examples = %d (%d actual, %d padding)",
                        len(eval_examples), num_actual_eval_examples,
                        len(eval_examples) - num_actual_eval_examples)
        tf.logging.info("  Batch size = %d", eval_batch_size)
        eval_steps = None
        eval_drop_remainder = False
        eval_input_fn = self.file_based_input_fn_builder(
            input_file=eval_file,
            seq_length=max_seq_length,
            is_training=False,
            drop_remainder=eval_drop_remainder)

        result = estimator.evaluate(input_fn=eval_input_fn, steps=eval_steps)
        output_eval_file = os.path.join(output_dir, "eval_results.txt")
        with tf.gfile.GFile(output_eval_file, "w") as writer:
            tf.logging.info("***** Eval results *****")
            for key in sorted(result.keys()):
                tf.logging.info("  %s = %s", key, str(result[key]))
                writer.write("%s = %s\n" % (key, str(result[key])))


if __name__ == '__main__':
    use_model = BertClassifier()
    use_model.run(output_dir="output_dir", save_summary_steps=10, save_checkpoints_steps=10, data_dir="../task",
                  train_batch_size=16, learning_rate=1e-5, num_train_epochs=5, max_seq_length=32, warmup_proportion=0.1,
                  mod="train", eval_batch_size=8)
