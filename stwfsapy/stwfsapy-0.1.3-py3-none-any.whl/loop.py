from rdflib import Graph
from rdflib.term import URIRef
from stwfsapy.predictor import StwfsapyPredictor
from stwfsapy import thesaurus as t
from stwfsapy import expansion
from stwfsapy import case_handlers
from stwfsapy.automata import nfa, conversion, construction

if __name__ == '__main__':
    graph = Graph()
    graph.load('/home/fuer/Annif-tutorial/data-sets/yso-nlf/yso-skos.rdf')
    langs = frozenset(['en'])
    all_deprecated = set(t.extract_deprecated(graph))
    concepts = set(t.extract_by_type_uri(
        graph,
        URIRef('http://www.w3.org/2004/02/skos/core#Concept'),
        remove=all_deprecated))
    print(len(concepts))
    labels = t.retrieve_concept_labels(
        graph,
        allowed=concepts,
        langs=langs)

    case_handler = case_handlers.title_case_handler
    expansion_funs = expansion.collect_expansion_functions(
        extract_upper_case_from_braces=True,
        extract_any_case_from_braces=False,
        expand_ampersand_with_spaces=True,
        expand_abbreviation_with_punctuation=True,
        simple_english_plural_rules=False
    )
    for concept, label in labels:
        expanded = label
        for expansion_fun in expansion_funs:
            expanded = expansion_fun(expanded)
        automata = nfa.Nfa()
        construction.ConstructionState(automata, case_handler(expanded), str(concept)).construct()
        try:
            automata.remove_empty_transitions()
        except:
            print(label)
            print(f'\t{expanded}')
            print(f'\t{case_handler(expanded)}')
        
    