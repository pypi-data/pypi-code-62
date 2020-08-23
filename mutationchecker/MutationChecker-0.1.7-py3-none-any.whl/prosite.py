import os
import requests

# Base URL for the REST accession to PRosite.
base_url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi"

def PrositeRequest(uniprot_id): 

    """
    This function takes an uniprot id, and returns a JSON with information of the prosite maches.

    @ input - Uniprot ID (str) - String of the uniprot identifier of the protein to check.

    @ output - JSON response of Prosite server with information about the found domains.
    """

    response = requests.get( base_url + "?seq=" + uniprot_id + "&output=json")
    decodedResponse = response.json()
    return decodedResponse

def CheckMutationProsite(num_residue, uniprot_id):

    """
    This function takes a number of the residue in the sequence according to uniprot, and a uniprot ID of the protein.
    It search the Prosite database to extract the motifs, and checks if the mutation falls in place.

    @ input - num_residue (int) - Number of the residue to check in the sequence
              uniprot_id (str) - String of the uniprot identifier of the protein to check.

    @ output - Bool - The "num_residue" falls into the domain found by Prosite
    """

    json = PrositeRequest(uniprot_id)

    for motif in json["matchset"]:

        is_element_inside = (num_residue >= motif["start"] and num_residue <= motif["stop"] )

        return is_element_inside

    print ("No domain motifs have been found in the query.")
    return None

def RetrieveDomain(num_residue, uniprot_id):

    """
    This function takes a number of the residue in the sequence according to uniprot, and a uniprot ID of the protein.
    It search the Prosite database to extract the motifs, and checks if the mutation falls in place.

    @ input - num_residue (int) - Number of the residue to check in the sequence
              uniprot_id (str) - String of the uniprot identifier of the protein to check.

    @ output - tupple of str - Tupple with the parameters (Name of the domain found at num_residue, Accession code of Prosite of the domain.)
    """

    json = PrositeRequest(uniprot_id)

    for motif in json["matchset"]:

        is_element_inside = (num_residue >= motif["start"] and num_residue <= motif["stop"] )

        if is_element_inside:

            return (motif["signature_id"], motif["signature_ac"])

    print ("No motifs have been found for that residue.")
    return None
