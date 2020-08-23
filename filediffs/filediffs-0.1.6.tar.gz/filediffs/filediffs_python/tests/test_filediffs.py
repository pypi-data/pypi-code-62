from pathlib import Path
from time import time

from filediffs.filediffs_python.filediffs import file_diffs


def test_file_diffs_are_created():
    # arrange
    fp1 = str(Path(__file__).parent / "data" / "file_1.txt")
    fp2 = str(Path(__file__).parent / "data" / "file_2.txt")

    # outfile path for cleanup
    outfile_p_both = Path(__file__).parent / "lines_present_in_both_files.txt"
    outfile_p_1 = Path(__file__).parent / "lines_present_only_in_file1.txt"
    outfile_p_2 = Path(__file__).parent / "lines_present_only_in_file2.txt"

    # act
    lines_only_in_file_1, lines_only_in_file_2 = file_diffs(
        filename_1=fp1, filename_2=fp2,
        outpath_lines_present_in_both_files=str(outfile_p_both),
        outpath_lines_present_only_in_file1=str(outfile_p_1),
        outpath_lines_present_only_in_file2=str(outfile_p_2),
        verbose=False
    )

    # assert
    assert outfile_p_both.exists()
    assert outfile_p_1.exists()
    assert outfile_p_2.exists()

    lines_f1 = []
    with open(outfile_p_1) as fcon1:
        for line in fcon1:
            lines_f1.append(bytes(line, "utf-8"))

    lines_f2 = []
    with open(outfile_p_2) as fcon2:
        for line in fcon2:
            lines_f2.append(bytes(line, "utf-8"))

    lines_f_both = []
    with open(outfile_p_both) as fconb:
        for line in fconb:
            lines_f_both.append(bytes(line, "utf-8"))

    assert lines_f1 == [
        b'"1";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"2";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"3";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"4";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"5";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"6";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"7";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"8";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"9";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"10";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228'
        b';-0.0108214718366451\n']

    assert lines_f2 == [
        b'"16";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"17";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"18";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"19";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"20";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n']

    assert lines_f_both == [
        b'"V1";"V2";"V3";"V4";"V5";"V6"\n',
        b'"11";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;'
        b'-0.00902026455295847;-0.00902026455295847\n',
        b'"12";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;'
        b'-0.00902026455295847;-0.00902026455295847\n',
        b'"13";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;'
        b'-0.00902026455295847;-0.00902026455295847\n',
        b'"14";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;'
        b'-0.00902026455295847;-0.00902026455295847\n',
        b'"15";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;'
        b'-0.00902026455295847;-0.00902026455295847\n']

    # acleanup
    outfile_p_both.unlink()
    outfile_p_1.unlink()
    outfile_p_2.unlink()


def test_file_diffs_python_output():
    # arrange
    fp1 = str(Path(__file__).parent / "data" / "file_1.txt")
    fp2 = str(Path(__file__).parent / "data" / "file_2.txt")

    # outfile path for cleanup
    outfile_p_both = Path(__file__).parent / "lines_present_in_both_files.txt"
    outfile_p_1 = Path(__file__).parent / "lines_present_only_in_file1.txt"
    outfile_p_2 = Path(__file__).parent / "lines_present_only_in_file2.txt"

    # act
    lines_only_in_file_1, lines_only_in_file_2 = file_diffs(
        filename_1=fp1, filename_2=fp2,
        outpath_lines_present_in_both_files=str(outfile_p_both),
        outpath_lines_present_only_in_file1=str(outfile_p_1),
        outpath_lines_present_only_in_file2=str(outfile_p_2),
        verbose=False
    )

    assert lines_only_in_file_1 == [
        b'"1";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"2";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"3";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"4";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"5";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"6";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"7";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"8";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"9";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228;'
        b'-0.0108214718366451\n',
        b'"10";-0.0106417702666228;-0.0106417702666228;-0.0106417702666228;-0.0108214718366451;-0.0106417702666228'
        b';-0.0108214718366451\n']
    assert lines_only_in_file_2 == [
        b'"16";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"17";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"18";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"19";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n',
        b'"20";-0.00848124395493423;-0.00866091748760897;-0.00866091748760897;-0.00902026455295847;-0.009020264552'
        b'95847;-0.00902026455295847\n']

    # acleanup
    outfile_p_both.unlink()
    outfile_p_1.unlink()
    outfile_p_2.unlink()


def test_file_diffs_performance():
    # arrange
    fp1 = str(Path(__file__).parent / "data" / "file_1.txt")
    fp2 = str(Path(__file__).parent / "data" / "file_2.txt")

    # outfile path for cleanup
    outfile_p_both = Path(__file__).parent / "lines_present_in_both_files.txt"
    outfile_p_1 = Path(__file__).parent / "lines_present_only_in_file1.txt"
    outfile_p_2 = Path(__file__).parent / "lines_present_only_in_file2.txt"

    # act
    start = time()
    runtime_avg = []
    for i in range(0, 10000):
        start_loop = time()
        lines_only_in_file_1, lines_only_in_file_2 = file_diffs(
            filename_1=fp1, filename_2=fp2,
            outpath_lines_present_in_both_files=str(outfile_p_both),
            outpath_lines_present_only_in_file1=str(outfile_p_1),
            outpath_lines_present_only_in_file2=str(outfile_p_2),
            verbose=False
        )
        runtime_avg.append(time() - start_loop)
    runtime = time() - start
    # Todo: check runtime on Travis/centOS/manylinux. locally the function is fast
    print(runtime)
    assert True
    # asserts
    # runtime for 10.000 times file diff of two files with each having 10 lines and 5 lines differ is < 20s
    # assert runtime < 20
    # assert average is smaller than 20/10.000
    # assert sum(runtime_avg) / len(runtime_avg) <= 20 / 10000

    # acleanup
    outfile_p_both.unlink()
    outfile_p_1.unlink()
    outfile_p_2.unlink()

# __file__ = 'filediffs/tests/test_comparefiles.py'
