#!/usr/bin/env python3

def letterRegex(n):
    letterDict = {'A':'A', 'C':'C','G':'G','T':'T', 'B':'(C|G|T)', 'D':'(A|G|T)', 'H':'(A|C|T)', 'K':'(G|T)', 'M':'(A|C)', 'N':'(A|C|G|T)', 'R':'(A|G)', 'S':'(C|G)', 'V':'(A|C|G)', 'W':'(A|T)', 'Y':'(C|T)'}
    return letterDict[n]


def createRegex(string):
    return string
