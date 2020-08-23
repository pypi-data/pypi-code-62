import os
import requests
import Bio
from Bio.PDB import PDBList, PDBParser
from Bio.Data.IUPACData import protein_letters_3to1
from Bio.pairwise2 import format_alignment
from Bio import pairwise2
from xml.etree import ElementTree

def DownloadPDB(pdb_id): 

    """
    This function takes as input a PDB ID (Can accept both one id in str format, or a list of str ids.)
    If a list is submitted, it will check until it founds a downloadable PDB.
    
    @ input - pdb_id (str) OR pdb_id (list)
    @ output - Path to PDB file. (str)
    """

    if not isinstance(pdb_id, list): pdb_id = [pdb_id]

    length_dict = dict()
    pdbl=PDBList()

    # First check which is the one with longest structure
    for identifier in pdb_id:
        if identifier == "" or len(identifier) != 4:
            continue
        response = requests.get("https://www.rcsb.org/pdb/rest/describeMol?structureId=" + identifier)
        tree = ElementTree.fromstring(response.content)
        length_dict[identifier] = tree[0][0].attrib["length"]
    
    longest_pdb = max(length_dict, key=length_dict.get)

    filename = pdbl.retrieve_pdb_file(longest_pdb, pdir=".", file_format="pdb")
     
    return filename

def PDBtoSequence(pdb_file):   
    
    """
    This function takes a path to a PDB file and extract its fasta. 
    @ input - pdb_file (str) : Path to PDB file
    @ output - fasta (str) : Fasta of the PDB file
    """

    def _residue_parser(res):   
        """
        Internal Helper function for the parsing of residues of the PDB file
        """
        if res.get_resname().title() == "Hoh":
            return ""
        try:
            return protein_letters_3to1[res.get_resname().title()]
        except :
            return "X"

    #Check that file exists.
    if not (os.path.exists(pdb_file)): 
        print ("The file does not exist.")
        return None

    # Check that the file has a file format of PDB or ENT
    if not (pdb_file.endswith(".pdb") or pdb_file.endswith(".ent")): 
        print ("The file is not a .pdb or .ent file.")
        return None  

    parser = PDBParser(PERMISSIVE=1)
    residues = parser.get_structure('X', pdb_file).get_residues()
    resid_1_letter = map(lambda res: _residue_parser(res) , residues)
    
    return "".join(resid_1_letter)

def MapUniprotToPDB(uniprot_sequence, pdb_sequence, res_mut): 

    """
    This function takes the sequence of uniprot, the sequence of PDB and a list of residue numbers of uniprot, and check if these residue have structure in the PDB file
    @ input - uniprot_sequence (str) - Uniprot Fasta sequence
    @ input - pdb_sequence (str) - PDB Fasta Sequence
    @ input - res_mut_num_list - List of residues of Uniprot Sequence
    @ output - list - List of residues with structure in PDB Sequence. If "-" means, no structure.
    """

    PDB_residues = list()
    alignments = pairwise2.align.globalms(uniprot_sequence, pdb_sequence, 2, -1, -5, -.1)

    if isinstance(res_mut, int):
        res_mut = [res_mut]
    
    for mutation in res_mut:
        if alignments[0][1][int(mutation)-1] != "-":
            subsequence = alignments[0][1][:int(mutation)]
            GAPnum = subsequence.count("-")
            PDBresidue = int(mutation) - int(GAPnum)
            PDB_residues.append(int(PDBresidue))
        else:
            continue
    
    return PDB_residues

def CheckDistances(res_id_1, ResiduesList, pdb_file):

    """
    This function takes the number of a residue inside a PDB file, the number of ActiveSiteResidues in a PDB file, and a PDB file, and returns 
    the list of distances from res_id_1 to each of the Active Site Residues in Amstrongs.
    
    @ input - res_id_1 (int) - Residue number of the mutation
    @ input - ActiveSiteResidues (list) - List of the active site residue numbers (List of int)
    @ input - pdb_file (str) - Path to PDB file

    @ output - List of floats: List of distances from res_id_1 to each of the ActiveSiteResidues in Amstrongs.
    """

    parser = PDBParser()
    structure = parser.get_structure("X", pdb_file)

    mutation_CA = list(structure.get_residues())[int(res_id_1)-1]['CA']

    if len(ResiduesList) == 0:
        print ("Active Site residues are not in the structure. Halting execution")
        return None
        
    return list(map(lambda res: (str(list(structure.get_residues())[int(res)-1].get_resname()) + str(int(res)) , round(float(list(structure.get_residues())[int(res_id_1)-1]['CA'] - list(structure.get_residues())[int(res)-1]['CA']), 2)) , ResiduesList))

