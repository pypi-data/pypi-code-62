from .pdf_rules import PDF
import sys

def main():
    filepath = sys.argv[1]
    pdf = PDF(filepath)
    print(pdf)
