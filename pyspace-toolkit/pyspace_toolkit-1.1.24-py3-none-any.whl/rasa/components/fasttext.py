# %%
import logging
import os
import typing
import warnings
from typing import Any, Dict, List, Optional, Text, Tuple, Type

import numpy as np
from scipy.sparse import csr_matrix

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

import rasa.utils.io as io_utils
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.classifiers import LABEL_RANKING_LENGTH
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.components import Component
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.constants import DENSE_FEATURE_NAMES, SPARSE_FEATURE_NAMES, TEXT
from rasa.nlu.featurizers.featurizer import sequence_to_sentence_features
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
import rasa.utils.common as common_utils

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    import sklearn

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pyspace_resources
import fasttext

import pickle
from sklearn.model_selection import train_test_split

from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Embedding, Bidirectional, Dropout, LSTM, Dense, TimeDistributed
from tensorflow.keras.optimizers import Adam



class FastText(IntentClassifier):
    # varying batch size
    # stratified batch
    # batch normalization layer
    # tqdm callback

    defaults = {
        'epoch' : 50,
        'dim' : 300,
        'minn' : 3,
        'maxn' : 6,
        'lr' : 0.01,
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        clf = None,
        le = None,
    ) -> None:

        super().__init__(component_config)
        self.clf = clf
        self.le = le


    def generate_data(self, intent_examples, train_predict='predict'):
        def write_fastext_dataset(X, y, path):
            # Create dataset
            with open(path, "w+", encoding='utf-8') as file:
                for text, label in zip(X, y):
                    file.write(f'__label__{label} {text}\n')


        labels = [e.get("intent") for e in intent_examples]
        self.le = LabelEncoder()
        y = self.le.fit_transform(labels)

        texts = [message.text for message in intent_examples]
        write_fastext_dataset(texts, y, './fasttext_dataset.txt')
        
        return './fasttext_dataset.txt'

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        fasttext_dataset = self.generate_data(training_data.intent_examples, train_predict='train')
        fasttextparameters = {
            'epoch' : self.component_config["epoch"],
            'dim' : self.component_config["dim"],
            'minn' : self.component_config["minn"],
            'maxn' : self.component_config["maxn"],
            'lr' : self.component_config["lr"],
        }
        self.clf = fasttext.train_supervised(input=fasttext_dataset, **fasttextparameters)
        # pretrainedVectors=fasttext_pretrained_path, 
        
    def process(self, message: Message, **kwargs: Any) -> None:
        """Return the most likely intent and its probability for a message."""

        X = [message.text]
                
        intent_ids, probabilities = self.predict(X)
        intents = self.le.inverse_transform(np.ravel(intent_ids))

        probabilities = probabilities.flatten()

        if intents.size > 0 and probabilities.size > 0:
            ranking = list(zip(list(intents), list(probabilities)))[
                :LABEL_RANKING_LENGTH
            ]

            intent = {"name": intents[0], "confidence": float(probabilities[0])}

            intent_ranking = [
                {"name": intent_name, "confidence": float(score)}
                for intent_name, score in ranking
            ]
        else:
            intent = {"name": None, "confidence": 0.0}
            intent_ranking = []

        import json
        intent = json.loads(json.dumps(intent))
        intent_ranking = json.loads(json.dumps(intent_ranking))
        message.set("intent", intent, add_to_output=True)
        message.set("intent_ranking", intent_ranking, add_to_output=True)

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Given a bow vector of an input text, predict most probable label.
        Return only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        sorted_indices, probabilities = self.clf.predict(X, k=-1)
        sorted_indices = [int(i.replace('__label__','')) for i in sorted_indices[0]]
        probabilities = probabilities[0]

        return sorted_indices, probabilities

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this model into the passed directory."""

        classifier_file_name = file_name + "_classifier.pkl"
        
        self.clf.save_model( os.path.join(model_dir, classifier_file_name) ) 

        preprocessing_file_name = file_name + "_preprocessing.pkl"
        preprocessing_variables = self.le.classes_
        
        with open(os.path.join(model_dir, preprocessing_file_name), 'wb') as f:
            pickle.dump(preprocessing_variables, f)

        return {"classifier": classifier_file_name, "preprocessing": preprocessing_file_name}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["KerasBiLSTM"] = None,
        **kwargs: Any,
    ) -> "KerasBiLSTM":
    
        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        preprocessing_file = os.path.join(model_dir, meta.get("preprocessing"))

        clf = fasttext.load_model(classifier_file)
        with open(preprocessing_file, 'rb') as f:
            classes = pickle.load(f)

        le = LabelEncoder()
        le.classes_ = classes

        return cls(meta, clf, le,)
