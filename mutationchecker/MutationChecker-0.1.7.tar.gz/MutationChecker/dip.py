import os
import requests

uniprot_url = "https://www.uniprot.org/uniprot/"

def GeneToDIP(gene_id, specie="HUMAN"): 

    """
    This function takes a str GENEID identifier, and a str SPECIE (default: Human) and returns the DIP accession code.
    . Returns \"\" if the identifier is not found or not has structure.
    
    @ input - gene_id (str)
    @ input - specie (str) OPTIONAL
    @ output - PDB id (str)
    """

    response = requests.get( uniprot_url + "?query=organism:" + specie + "+AND+gene_exact:" + gene_id + "+reviewed:yes&format=tab&columns=database(DIP)")
    first_identifier = response.content.decode('utf-8')
    if first_identifier == "":
        return ""
    else:
        identifiers = first_identifier.split("\n")[1].split(";")
        return identifiers[0]