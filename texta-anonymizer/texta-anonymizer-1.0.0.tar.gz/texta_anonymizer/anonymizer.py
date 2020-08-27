import regex as re

from .extractors.name_extractor import NameExtractor
from .synthesizers import Synthesizer
from .generators import InitialsGenerator

from .exceptions import InvalidInputError

from typing import List, Union, Dict, Tuple


SUPPORTED_EXTRACTORS = (
    "NAMES"
)

SUPPORTED_SUBSTITUTORS = (
    "FAKE_INIT"
)

SUPPORTED_SYNTHESIZERS = (
    "INITIAL"
)

class Anonymizer:
    def __init__(self,
            replace_misspelled_names: bool = True,
            replace_single_last_names: bool = True,
            replace_single_first_names: bool = True,
            misspelling_threshold: float = 0.9,
            mimic_casing: bool = True,
            num_replacement_letters: int = 2,
            replacement_separator: str = "."
        ):

        self.init_generator = InitialsGenerator(
                                    num_letters = num_replacement_letters,
                                    separator = replacement_separator
                              )

        self.name_extractor = NameExtractor(
                                    allow_fuzzy_matching = replace_misspelled_names,
                                    extract_single_last_names = replace_single_last_names,
                                    extract_single_first_names = replace_single_first_names,
                                    fuzzy_threshold = misspelling_threshold,
                                    mimic_casing = mimic_casing
                              )

        self.synthesizer = Synthesizer()

    def _format_names(self, names: Union[List[str], List[Dict[str,str]]]) -> List[Dict[str,str]]:
        """ Format input names as List[Dict[str, str]] for further processing.

            Parameters:
                names - names to format
            Returns:
                formatted_names - formatted names
        """
        formatted_names = []
        for name in names:
            if isinstance(name, str):
                if "," not in name:
                    raise InvalidInputError(exit_code=3, msg="Incorrect format for names. Correct format is 'last_name, first_name'.")
                last_name, first_name = name.split(",")
                new_name = {"last_name": last_name.strip(), "first_name": first_name.strip()}
                formatted_names.append(new_name)
            elif isinstance(name, dict):
                if not "last_name" in name:
                    raise InvalidInputError(exit_code=4, msg="Missing required key 'last_name' in name.")
                if not "first_name" in name:
                    raise InvalidInputError(exit_code=5, msg="Missing required key 'first_name' in name.")
                formatted_names.append(name)
        return formatted_names


    def anonymize(self, text: str, names: Union[List[str], List[Dict[str,str]]]) -> str:
        """ Anonymize given names in given text.

            Parameters:
                text - text to anonymize
                names - list of names to anonymize,
                        e.g [{'first_name': 'Adolf', 'last_name': 'Hitler'}]
            Returns:
                anonymized_text - text where given names are anonymized

        """
        names = self._format_names(names)
        n = len(names)

        replacers = self.init_generator.generate(n)
        for i, name in enumerate(names):
            replacer = replacers[i]
            full_name = f"{name['first_name']} {name['last_name']}"
            name_matches = self.name_extractor.extract(text, name)
            for name_match in name_matches:
                replacer_in_correct_form = self.synthesizer.synthesize(name_match, full_name, replacer, "INITIALS")
                text = re.sub(name_match, replacer_in_correct_form, text)
        anonymized_text = text
        return anonymized_text
