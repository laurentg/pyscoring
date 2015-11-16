#!/usr/bin/python
import math
import sys

# Raw scores
# SCORES[i][j]: score given by i to j
# Standard example
S1 = (
	#  A   B   C   D  !E  !F
	# 20  20  30  40  30  10
	( -1, 20, 25, 30, 20, 10 ), # A
	( 20, -1, 30, 40, 30, 10 ), # B
	( 20, 10, -1, 50, 20,  5 ), # C
	( 10, 20, 30, -1, 20, 10 ), # D
	(  0,  0,  0,  0, -1, 50 ), # E
	(  0,  0,  0, 10, 40, -1 ), # F
)
# 2 groups
S2 = (
	# Z   A   B   C   D  !E  !F
	# 20 20  20  30  40  30  10
	( -1, 20, 40,  0,  0,  0,  0 ), # Z
	( 10, -1, 20, 40,  0,  0,  0 ), # A
	( 10, 20, -1, 40,  0,  0,  0 ), # B
	( 10, 20, 20, -1,  0,  0,  0 ), # C
	(  0,  0,  0,  0, -1, 50, 50 ), # D
	(  0,  0,  0,  0, 50, -1, 50 ), # E
	(  0,  0,  0,  0, 50, 50, -1 ), # F
)
# Bigger example
S3 = (
	#  A   B   C   D   E   F   G   H   I
	# 20  25  30  40  30  10  10  40  25
	( -1, 25, 30, 40, 30, 10, 10, 40, 25 ), # A Fairest
	( 20, -1, 30, 40, 30, 11, 10, 40, 25 ), # B Fairest
	( 25, 20, -1, 45, 30,  5, 15, 45, 20 ), # C Somehow fair
	( 20, 25, 35, -1, 20, 15, 10, 40, 25 ), # D Fair
	( 10, 15, 35, 40, -1, 10, 12, 30, 25 ), # E Fair
	( 10, 10, 10, 50, 30, -1, 20, 30, 20 ), # F Exaggerate
	( 20, 20, 20, 20, 20, 20, -1, 20, 20 ), # G Indecise
	(  0,  0,  0,  0,  0, 50, 50, -1,  0 ), # H Cheater with F/G
	(  5,  5, 10, 60, 20,  5,  5,  5, -1 ), # I Not fair
)
# Which set to use?
S0 = S3

# Magic constants
sigma0 = 1.0     # "normal standard deviation"

N = len(S0)

def print_vector(name, V):
	sys.stdout.write("%s [ " % name)
	for i in xrange(0, len(V)):
		if (V[i] < 0):
			sys.stdout.write(" --")
		else:	sys.stdout.write("%3d" % math.trunc(V[i] * 100))
		if i < len(V) - 1:
			sys.stdout.write(", ")
	sys.stdout.write(" ] \n")

# Normalize scores
S = [ [ 1.0 for i in xrange(0, N) ] for j in xrange(0, N) ]
for i in xrange(0, N):
	sum = 0.0
	for j in xrange(0, N):
		if i != j:
			sum += S0[i][j]
	for j in xrange(0, N):
		if i != j:
			S[i][j] = S0[i][j] * 1.0 * (N - 1) / sum
		else:	S[i][j] = -1.0

first = True
for s in S:
	print_vector("Scoring matrix: " if first else "                ", s)
	first = False
sys.stdout.write("\n")

# Start with weight 1.0 for everybody
W = [ 1.0 for i in xrange(0, N) ]
Z = [ 1.0 for i in xrange(0, N) ]

for n in xrange(0, 20):
	# Compute average score
	R = [ 0.0 for i in xrange(0, N) ]
	for j in xrange(0, N): # compute average of Pj
		assum = 0.0
		wzsum = 0.0
		for i in xrange(0, N): # given by all Pi
			if i != j:
				wz = W[i] * Z[i]
				assum += wz * S[i][j]
				wzsum += wz
		R[j] = assum / wzsum

	# Normalize average score R
	rsum = 0.0
	for i in xrange(0, N):
		rsum += R[i]
	for i in xrange(0, N):
		R[i] = R[i] * N / rsum

	# Compute standard deviation between score and average:
	# "goodwill factor"
	for i in xrange(0, N): # Scorer Pi
		sigma = 0.0
		for j in xrange(0, N): # Scored Pj
			if i != j:
				delta = R[j] - S[i][j]
				sigma += delta * delta
		sigma = math.sqrt(sigma / N)
		W[i] = math.exp(-sigma / sigma0)
		Z[i] = R[i]

	# Normalize weights
	wsum = 0.0
	for i in xrange(0, N):
		wsum += W[i]
	for i in xrange(0, N):
		W[i] = W[i] * N / wsum

	# Print results
	if n == 0:
		print_vector("Raw scores:     ", R)

# Final score is average score adjusted by a "punishment factor"
RR = [ 0.0 for i in xrange(0, N) ]
for i in xrange(0, N):
	RR[i] = R[i] * W[i]
rrsum = 0.0
for i in xrange(0, N):
	rrsum += RR[i]
for i in xrange(0, N):
	RR[i] = RR[i] * N / rrsum
print_vector("Adjusted scores:", R)
print_vector("Punished scores:", RR)
print_vector("Fairness factor:", W)
