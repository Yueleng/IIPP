'''
Algorithmic Thinking, Part II
Project 4. Computing global and local alignments

@author: Yueleng & Kexin
'''


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
	'''
	@input:
	a set of characters alphabet: A C G T - or Sigma union -
	diag_score: M_{sigma, sigma}
	off_diag_score: M_{sigma, sigma'}
	dash_score: M_{sigma, -} = M_{-, sigma}

	@output: distionary of dictionaries.
	'''
	scores = {}
	scores['-'] = {'-': dash_score}

	for let_a in alphabet:
		if let_a not in scores:
			scores[let_a] = {} #create a dictionary under scores[let_a]
		scores[let_a]['-'] = dash_score
		scores['-'][let_a] = dash_score

		# Fill in other keys for dictionary: scores[let_a]
		for let_b in alphabet:
			if let_a == let_b:
				scores[let_a][let_b] = diag_score
			else:
				scores[let_a][let_b] = off_diag_score

	return scores

def _clip(value, global_flag):
	'''
	Limit values to 0 when global_flag is not set
	'''
	return value if global_flag else max(0, value)


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
	'''
	@input:
	seq_x, seq_y: whose elements share a common alphabet with the scoring matirx 
	scoring matrix: output of func build_scoring_matrix
	global_flag: True/False. 
				 if True, use Algorithm from Q8
				 if False, use Algorithm from Q12, i.e. S[i,j] assigned with 0 if negative.
	'''
	rows, cols = len(seq_x), len(seq_y)

	#initialize alignment
	#first row and first column not used!
	alignment = [[0 for _ in range(cols + 1)] for _ in range(rows + 1)]
	for idx_i in range(1, rows + 1):
		alignment[idx_i][0] = _clip(alignment[idx_i - 1][0] + scoring_matrix[seq_x[idx_i - 1]]['-'], global_flag)

	for idx_j in range(1, cols + 1):
		alignment[0][idx_j] = _clip(alignment[0][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]], global_flag)

	for idx_i in range(1, rows + 1):
		for idx_j in range(1, cols + 1):
			alignment[idx_i][idx_j] = max([
				_clip(alignment[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]], global_flag),
				_clip(alignment[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-'], global_flag),
				_clip(alignment[idx_i][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]], global_flag)
				])

	return alignment

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	'''
	@input:
	seq_x, seq_y: whose elements share a common alphabet with the scoring matirx;
	scoring matrix: output of func build_scoring_matrix;
	alignment matrix: output of func compute_global_alignment;

	@output: tuple of the form (score, align_x, align_y)
	where score is the score of the global alignment,
	align_x and align_y should have the same length and may include 
	the padding characters '-';
	'''
	return compute_alignment(seq_x, seq_y,
							 scoring_matrix,
							 alignment_matrix,
							 global_flag = True)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	'''
	See Q13 of Homework.
	Start the traceback from the entry in S that has the maximum value over the entire matrix 
	and trace backwards using exactly the same technique as in ComputeGlobalAlignment. 
	Stop the traceback when the first entry with value 0 is encountered. 
	If the local alignment matrix has more than one entry that has the maximum value, 
	any entry with maximum value may be used as the starting entry.
	'''
	return compute_alignment(seq_x, seq_y,
							 scoring_matrix,
							 alignment_matrix,
							 global_flag = False)


def compute_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix, global_flag):
	'''
	Universal function for computing global and local alignments
	'''
	idx_i, idx_j = len(seq_x), len(seq_y)
	if not global_flag:
		# i.e. global_flag == False, which means the local case.
		idx_i, idx_j = max_index(alignment_matrix, len(seq_x), len(seq_y))
	best_score = alignment_matrix[idx_i][idx_j]
	new_xs, new_ys = '', ''

	def cond_global(idx_i, idx_j):
		'''
		Condition for while loops in global mode
		'''
		if idx_j is None:
			return idx_i != 0
		elif idx_i is None:
			return idx_j != 0
		else:
			return idx_i != 0 and idx_j != 0

	def cond_local(idx_i, idx_j):
		'''
		Condition for while loops in local mode
		'''
		return alignment_matrix[idx_i][idx_j] != 0

	cond = cond_global if global_flag else cond_local

	while cond(idx_i, idx_j):
		if alignment_matrix[idx_i][idx_j] == _clip(alignment_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]], global_flag):
			new_xs = seq_x[idx_i - 1] + new_xs
			new_ys = seq_y[idx_j - 1] + new_ys
			idx_i, idx_j = idx_i - 1, idx_j - 1
		elif alignment_matrix[idx_i][idx_j] == _clip(alignment_matrix[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-'], global_flag):
			new_xs, new_ys = seq_x[idx_i - 1] + new_xs, '-' + new_ys
			idx_i -= 1
		else:
			new_xs, new_ys = '-' + new_xs, seq_y[idx_j - 1] + new_ys
			idx_j -= 1

	while cond(idx_i, None if global_flag else idx_j):
		new_xs, new_ys = seq_x[idx_i - 1] + new_xs, '-' + new_ys
		idx_i -= 1

	while cond(None if global_flag else idx_i, idx_j):
		new_xs, new_ys = '-' + new_xs, seq_y[idx_j - 1] + new_ys 
		idx_j -= 1

	return best_score, new_xs, new_ys


def max_index(alignment, rows, cols):
	'''
	Position of max item in the matrix
	'''
	max_i, max_j = 0, 0
	for idx_i in range(rows + 1):
		for idx_j in range(cols + 1):
			if alignment[idx_i][idx_j] > alignment[max_i][max_j]:
				max_i, max_j = idx_i , idx_j 

	return max_i, max_j



