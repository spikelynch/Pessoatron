#!/usr/bin/env python

import sys
from itertools import permutations
from collections import Counter
import pystache


# The synthemes were compiled by hand and the synthematic totals were taken
# from Greg Egan's diagram of the Tutt-Coxeter graph on this page by John
# Baez: https://math.ucr.edu/home/baez/six.html

SYNTHEMES = {
	"A": [ (1, 2), (3, 4), (5, 6) ],
	"B": [ (1, 2), (3, 5), (4, 6) ],
	"C": [ (1, 2), (3, 6), (4, 5) ],
	"D": [ (1, 3), (2, 4), (5, 6) ],
	"E": [ (1, 3), (2, 5), (4, 6) ],
	"F": [ (1, 3), (2, 6), (4, 5) ],
	"G": [ (1, 4), (2, 3), (5, 6) ],
	"H": [ (1, 4), (2, 5), (3, 6) ],
	"I": [ (1, 4), (2, 6), (3, 5) ],
	"J": [ (1, 5), (2, 3), (4, 6) ],
	"K": [ (1, 5), (2, 4), (3, 6) ],
	"L": [ (1, 5), (2, 6), (3, 4) ],
	"M": [ (1, 6), (2, 3), (4, 5) ],
	"N": [ (1, 6), (2, 4), (3, 5) ],
	"O": [ (1, 6), (2, 5), (3, 4) ]
	}

TOTALS = {
	"t1": [ "A", "F", "H", "J", "N" ],
	"t2": [ "A", "E", "I", "K", "M" ],
	"t3": [ "B", "D", "H", "L", "M" ],
	"t4": [ "B", "F", "G", "K", "O" ],
	"t5": [ "C", "E", "G", "L", "N" ],
	"t6": [ "C", "D", "I", "J", "O" ]	
}

PERM6 = list(permutations([1, 2, 3, 4, 5, 6]))

PERM6D = {}

for i in range(1, len(PERM6) + 1):
	PERM6D[i] = f'{PERM6[i - 1]}'

def nspan(i):
	return f'<span class="s{i}">{i}</span>'

def lookup_syntheme(s):
	c0 = Counter(s)
	for n, s1 in SYNTHEMES.items():
		c1 = Counter(s1)
		if c1 == c0:
			return n
	sys.stderr.write(f"mismatched syntheme {s}\n")
	return "-"


def lookup_synthematic_total(t):
	c0 = Counter(t)
	for n, t1 in TOTALS.items():
		c1 = Counter(t1)
		if c1 == c0:
			return n
	sys.stderr.write(f"mismatched total {t}\n")
	return "-"

def lookup_perm6(p):
	for n, p1 in PERM6D.items():
		if p1 == p:
			return n
	sys.stderr.write(f"mismatched perm {p}\n")
	return "-"

print("""
<html>
<head>
<link href="combos.css" rel="stylesheet" />
</head>
<body>
""")

sys.stderr.write("Permuting...\n")


i = 1

find_dups = {}

for p in PERM6:
	print(f'<h3>{i}: {p}</h3>')
	i += 1
	seq = ''
	for tname, t in TOTALS.items():
		print('<div class="row">' + tname + ": ")
		automorphism = []
		for s in t:
			rev = []
			ss = ''
			for x, y in SYNTHEMES[s]:
				x0 = p[x - 1]
				y0 = p[y - 1]
				ss = ss + '(' + nspan(x0) + ' ' + nspan(y0) + ')'
				if x0 > y0:
					z0 = x0
					x0 = y0
					y0 = z0
				rev.append(( x0, y0 ))
			rs = lookup_syntheme(rev)
			print(rs + ' ')
			automorphism.append(rs)
			seq += rs
		autot = lookup_synthematic_total(automorphism)
		print(f"--&gt;{autot}")
		print("</div>")
	if seq in find_dups:
		find_dups[seq] += 1
		sys.stderr.write("Duplicate " + seq + "\n")
	else:
		find_dups[seq] = 1
		print(f"<div>{seq}</div>")

print("\n")

print("""
</body>
</html>
""")
