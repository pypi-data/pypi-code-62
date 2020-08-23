import os
import requests

uniprot_url = "https://www.uniprot.org/uniprot/"

def GeneToUniprot(gene_id, specie="HUMAN"): 

    """
    This function takes a str GENEID identifier, and a str SPECIE (default: Human) and returns the Reviewed Entries Uniprot ID value. Returns \"\" if the identifier is not found or not has structure.
    
    @ input - gene_id (str)
    @ input - specie (str) OPTIONAL
    @ output - Uniprot Reviewed id (list)
    """

    response = requests.get( uniprot_url + "?query=organism:" + specie + "+AND+gene_exact:" + gene_id + "+reviewed:yes&format=tab&columns=id")
    first_identifier = response.content.decode('utf-8')
    if first_identifier == "":
        return ""
    else:
        return first_identifier.split("\n")[1].split(";")[0]

def GeneToPDB(gene_id, specie="HUMAN"): 

    """
    This function takes a str GENEID identifier, and a str SPECIE (default: Human) and returns the first PDB mapped in Uniprot. Returns \"\" if the identifier is not found or not has structure.
    
    @ input - gene_id (str)
    @ input - specie (str) OPTIONAL
    @ output - PDB id (str)
    """

    response = requests.get( uniprot_url + "?query=organism:" + specie + "+AND+gene_exact:" + gene_id + "+reviewed:yes&format=tab&columns=database(PDB)")
    first_identifier = response.content.decode('utf-8')
    if first_identifier == "":
        return ""
    else:
        identifiers = first_identifier.split("\n")[1].split(";")
        return identifiers

def GeneToFasta(gene_id, specie="Human"): 

    """
    This function takes a str GENEID identifier, and a str SPECIE (default: Human) and returns the Fasta sequence stored in Uniprot. Returns \"\" if the identifier is not found or not has structure.
    
    @ input - gene_id (str)
    @ input - specie (str) OPTIONAL
    @ output - Fasta string (str)
    """

    response = requests.get( uniprot_url + "?query=organism:" + specie + "+AND+gene_exact:" + gene_id + "+reviewed:yes&format=tab&columns=sequence")
    str_response = response.content.decode('utf-8')
    if str_response != "":
        sequence = str_response.split("\n")[1]
        return sequence
    else:
        return ""