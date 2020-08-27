# -*- coding: utf-8 -*-
import regex as re
from typing import List, Dict, Tuple, Union
from jellyfish import jaro_winkler


DEFAULT_CONF = {
    "allow_fuzzy_matching": True,
    "extract_single_last_names": True,
    "extract_single_first_names": True,
    "fuzzy_threshold": 0.9,
    "mimic_casing": True
    }

class NameExtractor:
    """ Extract all variations of person's name from text.
    """

    def __init__(self,
            allow_fuzzy_matching: bool = DEFAULT_CONF["allow_fuzzy_matching"],
            extract_single_last_names: bool = DEFAULT_CONF["extract_single_last_names"],
            extract_single_first_names: bool = DEFAULT_CONF["extract_single_first_names"],
            fuzzy_threshold: float = DEFAULT_CONF["fuzzy_threshold"],
            mimic_casing: bool = DEFAULT_CONF["mimic_casing"]
            ):

        self.fuzzy_matching = allow_fuzzy_matching
        self.fuzzy_threshold_ln = 0.6
        self.fuzzy_threshold_fn = 0.7

        self.allow_upper_case = True
        self.allow_title_case = True
        self.allow_whitespaces = True
        self.allow_delete_last = mimic_casing # Allow deleting last character of last name for mocking casing

        self.extract_single_last_names = extract_single_last_names
        self.extract_single_first_names = extract_single_first_names

        self.allow_extra_chars = mimic_casing # Allow extra chars at the end of each pattern to mock casing
        self.add_jw_check = True # Use jaro_winkler distance to validate matches
        self.jw_threshold = fuzzy_threshold

    def set_params(self, **kwargs):
        if "allow_fuzzy_matching" in kwargs:
            self.fuzzy_matching = kwargs["allow_fuzzy_matching"]
        if "extract_single_last_names" in kwargs:
            self.extract_single_last_names = kwargs["extract_single_last_names"]
        if "extract_single_first_names" in kwargs:
            self.extract_single_first_names = kwargs["extract_single_first_names"]
        if "fuzzy_threshold" in kwargs:
            self.fuzzy_threshold = kwargs["fuzzy_threshold"]
        if "mimic_casing" in kwargs:
            self.allow_extra_chars = kwargs["mimic_casing"]
            self.allow_delete_last = kwargs["mimic_casing"]

    def restore_default_conf(self):
        self.fuzzy_matching = DEFAULT_CONF["allow_fuzzy_matching"]
        self.extract_single_last_names = DEFAULT_CONF["extract_single_last_names"]
        self.extract_single_first_names = DEFAULT_CONF["extract_single_first_names"]
        self.fuzzy_threshold = DEFAULT_CONF["fuzzy_threshold"]
        self.allow_extra_chars =  DEFAULT_CONF["mimic_casing"]
        self.allow_delete_last = DEFAULT_CONF["mimic_casing"]

    def _identical_casing(self, c1: str, c2: str) -> bool:
        """ Check if chars c1 and c2 have identical casing.

            Parameters:
                c1 - char to compare against c2
                c2 - char to compare against c1

            Returns:
                identical_casing - boolean value indicating if c1 and c2 have
                                   identical casing.

        """
        identical_casing = False
        if c1.isupper() and c2.isupper():
            identical_casing = True
        elif c1.islower() and c2.islower():
            identical_casing = True
        return identical_casing

    def get_fuzzy_matches(self, text: str, word: str, ignore_case: bool = False, threshold: float = 0.9,
                                i_w: int = 1, d_w: int = 1, s_w: int = 1) -> List[str]:
        """ Get fuzzy matches of given word from given text.

        Parameters:
            text  - Text to search matches from.
            word  - Word (or phrase) to search from the text.
            ignore_case  - Ignore casing while searching.
            threshold - TODO
            i_w - Insertion weight.
            d_w - Deletion weight.
            s_w - Substitution weight.

        Returns:
            matches - List of all the fuzzy matches of word in text.
        """
        n_allowed_edits = int(len(word)*(1-threshold))

        edit_pattern = f"{{{i_w}i+{d_w}d+{s_w}s<={n_allowed_edits}}}"
        search_pattern = f"(?<=^|\s)({word}){edit_pattern}(?=\s|$|\W)"
        if self.allow_extra_chars:
            search_pattern = f"(?<=^|\s)({word}){edit_pattern}\S{{,6}}(?=\s|$|\W)"


        if ignore_case:
            matches = re.findall(search_pattern, text, re.IGNORECASE)
        else:
            matches = re.findall(search_pattern, text)
            # Don't allow first letter casing changes
            w0 = word[0]
            matches = [m for m in matches if self._identical_casing(m[0], w0)]

        return list(set(matches))

    def get_exact_matches(self, text: str, word: str, ignore_case: bool = False) -> List[str]:
        """ Get exact matches of given word from given text.

        Parameters:
            text - Text to search matches from.
            word - Word (or phrase) to search from the text.
            ignore_case - Ignore casing while searching.

        Returns:
            matches - List of all exact matches of word in text.
        """
        search_pattern = f"(?<=^|\s){word}(?=\s|$|\W)"
        if ignore_case:
            matches = re.findall(search_pattern, text, re.IGNORECASE)
        else:
            matches = re.findall(search_pattern, text)
        return list(set(matches))

    def _generate_initials_patterns(self, first_name: str, add_whitespaces: bool = True) -> Union[List[str], str]:
        """ Generate all possible initals pattern combinations based on person's
            first name, e.g:

            'John Dorian' -> ['J.D.', 'J.D', 'JD', J D', ...]

            Parameters:
                first_name - first name
                add_whitespaces - include patterns with whitespace separators.

            Returns:
                patterns - all possible forms of initials.
        """
        first_names = first_name.split()
        first_names_short = []  # A. - H.
        for fn in first_names:
            if add_whitespaces:
                initials = [f"{name[0].upper()}\s*\.?" for name in fn.split("-") if name]
                short_patterns = ["\s*-\s*".join(initials)]
            else:
                initials_1 = [f"{name[0].upper()}." for name in fn.split("-") if name]
                initials_2 = [f"{name[0].upper()}" for name in fn.split("-") if name]
                initials = initials_1 + initials_2
                short_pattern_1 = "-".join(initials_1)
                short_pattern_2 = "-".join(initials_2)
                short_patterns = [short_pattern_1, short_pattern_2]
            first_names_short.extend(short_patterns)
        if add_whitespaces:
            patterns = "\s*".join(first_names_short)

        else:
            patterns = first_names_short
        return patterns

    def _add_whitespace_pattern(self, name: str) -> str:
        """ Add whitespace pattern after each character, e.g:
            'John Smith' -> 'J\s+o\s+h\s+n\s+S\s+m\s+i\s+t\s+h'

            Parameters:
                name - name to add whitespace pattern to.

            Returns:
                whitespaced_name - name with whitespaces.
        """
        # First remove all whitespaces
        name_wo_whitespaces = "".join(name.split())

        # Generate pattern where each character is separated by
        # at least one whitespace.
        whitespaced_name = "\s+".join(list(name_wo_whitespaces))

        return whitespaced_name

    def _generate_upper_pattern(self, name: str) -> str:
        """ Generate pattern supporting uppercased matches.
        """
        # FOR LAST NAMES ?
        # John Dorian -> ["John", "Dorian"]
        subnames = [sn for sn in re.split("\s+|\W", name) if sn]
        subnames_upper = []
        for subname in subnames:
            # If person has more than one name and subname is shorter
            # than 4 allow lowercased letters for cases like "... van der ..."
            if len(subnames) > 1 and len(subname) <=3:
                subname_upper = f"(?:{subname.upper()}|{subname.lower()})"
            else:
                subname_upper = subname.upper()
            subnames_upper.append(subname_upper)
        separator_pattern = "(?:\s|-|–|–)+"
        upper_pattern = separator_pattern.join(subnames_upper)
        return upper_pattern

    def _generate_title_pattern(self, name: str) -> str:
        """ Generate pattern supporting title matches.
        """
        # FOR LAST NAMES ?
        # John Dorian -> ["John", "Dorian"]
        subnames = [sn for sn in re.split("\s+|\W", name) if sn]
        subnames_title = []
        for subname in subnames:
            # If person has more than one name and subname is shorter
            # than 4 allow lowercased letters for cases like "... van der ..."
            if len(subnames) > 1 and len(subname) <=3:
                subname_title = f"(?:{subname.title()}|{subname.lower()})"
            else:
                subname_title = subname.title()
            subnames_title.append(subname_title)
        separator_pattern = "(?:\s|-|–|–)+"
        title_pattern = separator_pattern.join(subnames_title)
        return title_pattern

    def get_name_patterns(self, name_forms: List[str]) -> List[str]:
        """ Generate patterns for each name form with allowed
            casings and whitespacing.
        """
        name_patterns = []
        for name_form in name_forms:
            if self.allow_upper_case:
                # JOHN DORIAN SMITH
                upper_pattern = self._generate_upper_pattern(name_form)
                name_patterns.append(upper_pattern)

            if self.allow_title_case:
                # John Dorian Smith
                title_pattern = self._generate_title_pattern(name_form)
                name_patterns.append(title_pattern)

            if self.allow_whitespaces:
                # J O H N   D O R I A N  S M I T H
                if self.allow_upper_case:
                    upper_pattern_ws = self._add_whitespace_pattern(name_form.upper())
                    name_patterns.append(upper_pattern_ws)
                # J o h n  D o r i a n  S m i t h
                if self.allow_title_case:
                    title_pattern_ws = self._add_whitespace_pattern(name_form.title())
                    name_patterns.append(title_pattern_ws)

        # Remove duplicates
        name_patterns = list(set(name_patterns))
        return name_patterns

    def _combine_name_patterns(self, first_name_patterns: List[str], last_name_patterns: List[str]) -> List[str]:
        """ Combine first and last name patterns into one.
        """
        combined_name_patterns = []
        for fn_pattern in first_name_patterns:
            for ln_pattern in last_name_patterns:
                new_pattern = f"(?:{fn_pattern}\s*{ln_pattern})"
                combined_name_patterns.append(new_pattern)
        return combined_name_patterns


    def generate_pattern(self, first_name: str, last_name: str, text: str) -> str:
        """ Generate pattern covering all combinations of one name.
        """

        last_names = [last_name]
        first_names = [first_name]

        name_patterns = []

        if self.allow_delete_last:
            last_names.append(last_name[:-1])

        # If fuzzy matching is allowed, collect all variations of the name
        if self.fuzzy_matching:
            last_name_matches = self.get_fuzzy_matches(text, last_name, threshold=self.fuzzy_threshold_ln)
            first_name_matches = self.get_fuzzy_matches(text, first_name, threshold=self.fuzzy_threshold_fn)

            last_names.extend(last_name_matches)
            first_names.extend(first_name_matches)

            last_names = list(set(last_names))
            first_names = list(set(first_names))


        first_name_patterns = self.get_name_patterns(first_names)
        last_name_patterns = self.get_name_patterns(last_names)

        initials_patterns = self._generate_initials_patterns(first_name)
        first_name_patterns.append(initials_patterns)

        # order: first_name last_name, e.g. John Smith
        combined_name_patterns_1 = self._combine_name_patterns(first_name_patterns, last_name_patterns)

        # order: last_name first_name, e.g. Smith John
        combined_name_patterns_2 = self._combine_name_patterns(last_name_patterns, first_name_patterns)
        name_patterns.extend(combined_name_patterns_1)
        name_patterns.extend(combined_name_patterns_2)

        if self.extract_single_last_names:
            name_patterns.extend(last_name_patterns)

        if self.extract_single_first_names:
            name_patterns.extend(first_name_patterns)

        name_forms_with_endings = []

        # Allow one non-whitespace character at the end of each name
        updated_name_patterns = []
        for name_pattern in name_patterns:
            if self.allow_extra_chars:
                updated_name_pattern = f"{name_pattern}\S*"
            else:
                updated_name_pattern = f"{name_pattern}(?=\s)"
            updated_name_patterns.append(updated_name_pattern)

        pattern = "|".join(updated_name_patterns)

        return pattern


    def _filter_matches(self, name: Dict[str, str], matches: List[str]):
        filtered_matches = []
        first_name = re.sub(r"\s+", "", re.escape(name["first_name"])).lower()
        last_name  = re.sub(r"\s+", "", re.escape(name["last_name"])).lower()

        full_name = f"{first_name}{last_name}"

        first_name_inits = self._generate_initials_patterns(first_name, add_whitespaces=False)
        last_name_w_inits = [f"{fn_init.lower()}{last_name}" for fn_init in first_name_inits]

        #stripped_matches = [re.sub(r"\s+", "", re.escape(match)).lower() for match in matches]

        name_variations = [first_name, last_name, full_name] + last_name_w_inits
        name_variations = list(set(name_variations))

        matches.sort(key=lambda x:len(x))
        name_variations.sort(key=lambda x: len(x))

        for match in matches:
            stripped_match = re.sub("\s+", "", match).lower()

            for variation in name_variations:
                jw_distance = jaro_winkler(stripped_match, variation)
                if  jw_distance >= self.jw_threshold:
                    filtered_matches.append(match)
                    break
        return filtered_matches

    def _escape_parenthesis(self, text):
        text = re.sub("[()]", "", text)
        return text

    def extract(self, text: str, name: Dict[str, str]) -> List[str]:
        """ Extract all allowed variations of given name from the text.

            Parameters:
                text - text from where to extract variations of given name.
                name - name as a dict, e.g. {'last_name': 'Smith', 'first_name': 'John Dorian'}

            Returns:
                matches - list of all variations of the name found from the text.
        """
        patterns = []

        first_name = name["first_name"]
        last_name = name["last_name"]
        text = self._escape_parenthesis(text)

        pattern = self.generate_pattern(first_name, last_name, text)

        matches = re.findall(pattern, text)
        matches = [m for m in matches if m]
        matches = list(set(matches))

        if self.add_jw_check:
            matches = self._filter_matches(name, matches)

        matches.sort(key=lambda x: len(x), reverse=True)

        return matches
