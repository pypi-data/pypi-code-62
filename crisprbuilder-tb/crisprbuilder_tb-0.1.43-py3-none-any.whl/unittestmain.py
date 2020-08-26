import unittest
from os import remove, rename, path
from Bio import Entrez
from xmltodict import parse
from xlrd import open_workbook
from csv import reader
import subprocess

def change(nitro_base):
    if nitro_base == 'A':
        corresponding_base = 'T'
    elif nitro_base == 'T':
        corresponding_base = 'A'
    elif nitro_base == 'C':
        corresponding_base = 'G'
    elif nitro_base == 'G':
        corresponding_base = 'C'
    else:
        corresponding_base = nitro_base
    return corresponding_base

def concat(p_f1, p_f2, p_shuffled):
    with open(p_f1, 'r') as file_1, open(p_f2, 'r') as file_2, \
            open(p_shuffled, 'w') as f_shuffled:
        lignes_1 = file_1.readlines()
        for elt in lignes_1:
            f_shuffled.write(elt)
        lignes_2 = file_2.readlines()
        for elt in lignes_2:
            f_shuffled.write(elt)

def change_elt_file(path, suffixe, item):
    with open(path, 'r') as f_in, \
            open('tp.fasta', 'w') as f_out:
        lignes = f_in.readlines()
        for elt in lignes:
            ligne_finale = elt.replace(item + '.', item + suffixe + '.')
            f_out.write(ligne_finale)
    remove(path)
    rename('tp.fasta', path)

def add_spoligo_dico(type_sit, dico_afr, item, spol_sit):
    if type_sit == 'SIT':
        type_spoligo = 'spoligo'
    else:
        type_spoligo = 'spoligo_vitro'

    spol = dico_afr[item].get(type_spoligo)

    if spol in spol_sit:
        dico_afr[item][type_sit] = spol_sit.get(spol)
    else:
        dico_afr[item][type_sit] = 'X'

    print(f"We're adding the {type_sit}: {dico_afr[item][type_sit]} to the "
          f"database")

def get_info(srr):
    Entrez.email = "christophe.guyeux@univ-fcomte.fr"
    ret = Entrez.efetch(db="sra", id=srr, retmode="xml")
    dico = parse(ret.read())

    dico0 = {}
    location, date, sra, center, strain = '', '', '', '', ''

    if 'ILLUMINA' in dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
            'EXPERIMENT'].get('PLATFORM') and 'PAIRED' in dico[
                'EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                    'EXPERIMENT']['DESIGN']['LIBRARY_DESCRIPTOR'].get(
                        'LIBRARY_LAYOUT'):

        try:
            attributes = dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                                'SAMPLE']['SAMPLE_ATTRIBUTES'].get(
                                    'SAMPLE_ATTRIBUTE')
        except KeyError:
            return {}

        for k in attributes:
            if k.get('TAG') == 'geographic location (country and/or sea)':
                location = k.get('VALUE')
            elif k.get('TAG') == 'collection date':
                date = k.get('VALUE')
            elif k.get('TAG') == 'SRA accession':
                sra = k.get('VALUE')
            elif k.get('TAG') == 'Strain':
                strain = k.get('VALUE')

        center = dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
            'EXPERIMENT'].get('@center_name')

        if isinstance(
                dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']['STUDY'][
                    'IDENTIFIERS'].get('EXTERNAL_ID'), list):
            bioproject = dico['EXPERIMENT_PACKAGE_SET'][
                'EXPERIMENT_PACKAGE']['STUDY']['IDENTIFIERS']['EXTERNAL_ID'][0]\
                .get('#text', '')
        else:
            bioproject = dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'STUDY']['IDENTIFIERS']['EXTERNAL_ID'].get('#text', '')

        dico0 = {
            'location': location,
            'date': date,
            'SRA': sra,
            'center': center,
            'strain': strain,
            'taxid': dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'SAMPLE']['SAMPLE_NAME'].get('TAXON_ID', ''),
            'name': dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'SAMPLE']['SAMPLE_NAME'].get('SCIENTIFIC_NAME', ''),
            'study': dico['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE'][
                'STUDY'].get('@alias', ''),
            'bioproject': bioproject
        }
    return dico0

def to_brynildsrud():
    brynildsrud = {}
    source, author, study, location, date = '', '', '', '', ''
    p_brynildsrud = path.join(path.dirname(__file__), 'data',
                                 'Brynildsrud_Dataset_S1.xls')
    wwb = open_workbook(p_brynildsrud)
    wws = wwb.sheet_by_index(0)

    for row in range(1, wws.nrows):
        srr = wws.cell_value(row, 4)

        if len(srr) > 1:

            brynildsrud[srr] = {}
            source = wws.cell_value(row, 5).replace(',', '')

            if source == 'This study':
                author = 'Brynildsrud et al.'

            source = source.replace('This study', 'Global expansion of '
                                    'Mycobacterium tuberculosis lineage 4 '
                                    'shaped by colonial migration and local '
                                    'adaptation')

            if len(wws.cell_value(row, 3)) > 1:
                study = wws.cell_value(row, 3)

            if len(wws.cell_value(row, 6)) > 1:
                location = wws.cell_value(row, 6)

            if wws.cell_value(row, 0).count('_') == 2:
                dat = wws.cell_value(row, 0).split('_')[-1]
                une_date = True
                for elt in dat:
                    if elt not in '0123456789':
                        une_date = False
                if une_date:
                    date = dat

        brynildsrud[srr] = {
            'Source': source,
            'Author': author,
            'study accession number': study,
            'location': location,
            'date': date
        }
    return brynildsrud

def to_h37rv():
    p_nc = path.join(path.dirname(__file__), 'data', 'NC_000962.3.txt')
    with open(p_nc, 'r') as file:
        p_nc_reader = file.read()
    return p_nc_reader

H37RV = to_h37rv()

def to_reads(db_origine):
    lignee_renvoyee = {}
    P_CSV = path.join(path.dirname(__file__), 'data', 'lineage.csv')
    DEMI_LONGUEUR = 20

    with open(P_CSV, 'r') as file:
        csv_reader = reader(file, delimiter=',', quotechar='"')
        next(csv_reader)

        for row in csv_reader:
            if row[16] == db_origine and row[1] != '':
                lignee = row[0].strip()
                pos0 = int(row[1].strip())
                pos = pos0 - 1
                source = row[3].strip()[0]
                cible = row[3].strip()[2]
                assert H37RV[pos] == source
                seq1 = H37RV[pos - DEMI_LONGUEUR:pos + DEMI_LONGUEUR + 1]
                seq2 = seq1[:DEMI_LONGUEUR] + cible + seq1[DEMI_LONGUEUR + 1:]
                lignee_renvoyee[pos] = (seq1, seq2, lignee)

    print("We have selected specific reads to compare with different lineages")
    return lignee_renvoyee

def to_spol_sit():
    p_sorted = path.join(path.dirname(__file__), 'data', '1_3882_SORTED.xls')
    wwb = open_workbook(p_sorted)
    wws = wwb.sheet_by_index(0)
    spol_sit = {}

    for row in range(1, wws.nrows):
        spol, sit = wws.cell_value(row, 2).replace('n', '\u25A0').\
                        replace('o', '\u25A1'), wws.cell_value(row, 8)
        spol_sit[spol] = sit

    return spol_sit

def to_formatted_results(seq, repitem, nb_8_12):
    P_FASTA = path.join(path.dirname(__file__), 'tmp', 'snp.fasta')
    with open(P_FASTA, 'w') as file:
        file.write('>\n' + seq)
    result = subprocess.run(["blastn", "-num_threads", nb_8_12, "-query",
                             P_FASTA, "-evalue", "1e-5", "-task", "blastn",
                             "-db", repitem, "-outfmt", "10 sseq"],
                            stdout=subprocess.PIPE)

    return result.stdout.decode('utf8').splitlines()

def to_nb_seq(seq, chaine, debut_prefixe, fin_prefixe, debut_suffixe,
              fin_suffixe):
    return len([u for u in chaine if seq[fin_prefixe:fin_suffixe] in u]) + \
           len([u for u in chaine if seq[debut_prefixe:debut_suffixe] in u])




class CrisprMethods(unittest.TestCase):

    def test_len_reads(self):
        """
        Compares dico_afr[item]['len_reads'] with 108
        """
        item = 'ERR2704808'
        p_shuffled = path.join(path.dirname(__file__), 'REP', 'sequences',
                               item, item + '_shuffled.fasta')
        dico_afr = {}
        dico_afr[item] = {}
        if 'len_reads' not in dico_afr[item]:
            nb_len = len(
                ''.join(open(p_shuffled).read(10000).split('>')[1].split(
                    '\n')[1:]))
            dico_afr[item]['len_reads'] = nb_len
            self.assertEqual(dico_afr[item]['len_reads'], 108)

    def test_change(self):
        """
        Compares change('A') with 'T', change('T') with 'A', change('C') with
        'G', change('G') with 'C'
        """
        self.assertEqual(change("A"), "T")
        self.assertEqual(change("T"), "A")
        self.assertEqual(change("C"), "G")
        self.assertEqual(change("G"), "C")

    def test_concat(self):
        """
        Applies concat() to the tests files f1.txt and f2.txt and checks the
        content of f_shuffled.txt after processing.
        """
        concat("f1.txt", "f2.txt", "f_shuffled.txt")
        with open("f_shuffled.txt", 'r') as f:
            lignes = f.readlines()
        self.assertEqual(['ligne 1\n', 'ligne 2\n', 'ligne 3\n', 'ligne 4\n'],
                          lignes)

    def test_change_elt_file(self):
        """
        Applies change_elt_file() to the test file t.txt and checks the content
        of the file after processing.
        """
        change_elt_file("f.txt", "_1", "ERR2704808")
        with open("f.txt", 'r') as f:
            lignes = f.readlines()
        self.assertEqual(['ERR2704808_1.fasta\n', 'ERR2200220.fasta\n',
                          'ERR2704808_1.fasta\n'], lignes)

    def test_count_greater(self):
        """
        Counts the number of '>' in f_greater.txt, writes this number in
        sortie.txt and compares it to 2
        """
        with open("f_greater.txt", 'r') as f_in, open("sortie.txt", 'w') as \
                f_out:
            lignes = f_in.readlines()
            cpt = 0
            for elt in lignes:
                cpt += elt.count('>')
            f_out.write(str(cpt))
        nb_reads = eval(open("sortie.txt").read().split('\n')[0])
        self.assertEqual(nb_reads, 2)

    def test1_origines(self):
        """
        Fills out the data from Origines into the dictionary dico_afr[item]
        and checks the content of the dictionary after processing.
        """
        Origines = [
            {'Source': "Requete SRA avec txid78331[Organism:exp] (M.canettii)",
             'Author': "NCBI",
             'study accession number': '',
             'run accessions': ['ERR1336824', 'ERR1336825', 'ERR1336823']}
        ]
        item = 'ERR1336825'
        dico_afr = {}
        dico_afr[item] = {}
        for ref in Origines:
            if item in ref['run accessions']:
                for elt in ['Source', 'Author', 'study accession number',
                            'location']:
                    dico_afr[item][elt] = ref.get(elt)
        self.assertEqual(dico_afr[item]['Source'], 'Requete SRA avec '
                                                   'txid78331[Organism:exp] (M.canettii)')
        self.assertEqual(dico_afr[item]['Author'], 'NCBI')
        self.assertEqual(dico_afr[item]['study accession number'], '')
        self.assertEqual(dico_afr[item]['location'], None)

    def test2_Origines(self):
        """
        Checks that booleen_origines is True.
        """
        Origines = [
            {'Source': "Requete SRA avec txid78331[Organism:exp] (M.canettii)",
             'Author': "NCBI",
             'study accession number': '',
             'run accessions': ['ERR1336824', 'ERR1336825', 'ERR1336823']}
        ]
        item = 'ERR1336825'
        dico_afr = {}
        booleen_origines = False
        for k in Origines:
            if item in k['run accessions']:
                booleen_origines = True
                if 'location' in k:
                    dico_afr[item]['location'] = k.get('location')
        if booleen_origines:
            print(f"{item} is in the database Origines")
        else:
            print(f"{item} is not in the database Origines")
        self.assertEqual(booleen_origines, True)

    def test_get_info(self):
        """
        Fills out the data from NCBI into the dictionary dico0 and checks the
        content of the dictionary after processing.
        """
        self.assertEqual(get_info("ERR2704808")['location'], 'France')
        self.assertEqual(get_info("ERR2704808")['date'], '2007')
        self.assertEqual(get_info("ERR2704808")['SRA'], 'ERS2280688')
        self.assertEqual(get_info("ERR2704808")['center'], 'DST/NRF Centre of Excellence for Biomedical TB research, SAMRC Centre for TB Research')
        self.assertEqual(get_info("ERR2704808")['strain'], '')
        self.assertEqual(get_info("ERR2704808")['taxid'], '33894')
        self.assertEqual(get_info("ERR2704808")['name'], 'Mycobacterium ' \
                                                          'tuberculosis variant africanum')
        self.assertEqual(get_info("ERR2704808")['study'], 'ena-STUDY-DST/NRF ' \
                                                           'Centre of Excellence for Biomedical TB research, SAMRC Centre for TB Research-10-03-2018-12:26:21:907-341')
        self.assertEqual(get_info("ERR2704808")['bioproject'], 'PRJEB25506')

    def test_to_brynildsrud(self):
        """
        Compares elements of the dictionary brynildsrud with the database from
        the file data/Brynildsrud_Dataset_S1.xls.
        """
        self.assertEqual(to_brynildsrud()['ERR760595']['Source'], 'Eldholm (10.1038/ncomms8119)')
        self.assertEqual(to_brynildsrud()['ERR760595']['Author'], '')
        self.assertEqual(to_brynildsrud()['ERR760595']['study accession '
                                                       'number'], 'PRJEB7669')
        self.assertEqual(to_brynildsrud()['ERR760595']['location'], 'Argentina')
        self.assertEqual(to_brynildsrud()['ERR760595']['date'], '2005')

    def test_to_reads(self):
        """
        Checks the reads of lineage Shitikov 2.2 at the position 4280707
        extracted from lineage.csv.
        Checks that the result contains 3 elements for each position in the
        dictionary.
        """
        self.assertEqual(to_reads('Shiti')[4280707][0],
                         'TCGGGCACATTCTCCTCGCCGACGTAGGTGATCCGGGTTCC')
        self.assertEqual(to_reads('Shiti')[4280707][1],
                         'TCGGGCACATTCTCCTCGCCAACGTAGGTGATCCGGGTTCC')
        self.assertEqual(to_reads('Shiti')[4280707][2], '2.2')
        for elt in to_reads('Shiti'):
            self.assertEqual(len(to_reads('Shiti')[elt]), 3)

    def test_to_spol_sit(self):
        """
        Checks that '1' and '13' belong to the values of the dictionary returned
        after processing to_spol_sit(), but not '3'.
        """
        self.assertIn('1', to_spol_sit().values())
        self.assertIn('13', to_spol_sit().values())
        self.assertNotIn('3', to_spol_sit().values())

    def test_add_spoligo_dico(self):
        """
        Checks that the value of dico_afr['ERR2704808']['SIT'] is 'X' after
        processing add_spoligo_dico.
        """
        dico_afr = {
            'ERR2704808': {
                'spoligo': '',
                'SIT': ''
            }
        }
        add_spoligo_dico("SIT", dico_afr, "ERR2704808", to_spol_sit())
        self.assertEqual(dico_afr['ERR2704808']['SIT'], 'X')

    def test_to_formatted_results(self):
        """
        Compares to_formatted_results(seq, 'REP/sequences/ERR2704808/ERR2704808',
         '12')[2] and 'ACGTCGATGGTCGCGACCTCCGCGGCATAGTCGAA'
        """
        seq = 'ACGTCGATGGTCGCGACCTCCGCGGCATAGTCGAA'
        self.assertEqual(to_formatted_results(seq, 'REP/sequences/ERR2704808/ERR2704808',
         '12')[2], 'ACGTCGATGGTCGCGACCTCCGCGGCATAGTCGAA')

    def test_to_nb_seq(self):
        """
        Compares to_nb_seq(seq, formatted_result, 13, 17, 18, 22) and 616
        """
        seq = 'ACGTCGATGGTCGCGACCTCCGCGGCATAGTCGAA'
        formatted_result = to_formatted_results(seq,
                                                'REP/sequences/ERR2704808/ERR2704808', '12')
        to_nb_seq(seq, formatted_result, 13, 17, 18, 22)
        self.assertEqual(to_nb_seq(seq, formatted_result, 13, 17, 18, 22), 616)


if __name__ == '__main__':
    unittest.main()



