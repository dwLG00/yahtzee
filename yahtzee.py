import itertools
import random

def is_yahtzee(*roll):
	return roll[0] == roll[1] == roll[2] == roll[3] == roll[4]

def is_four(*roll):
	return (
		roll[0] == roll[1] == roll[2] == roll[3] or
		roll[0] == roll[1] == roll[2] == roll[4] or
		roll[0] == roll[1] == roll[3] == roll[4] or
		roll[0] == roll[2] == roll[3] == roll[4] or
		roll[1] == roll[2] == roll[3] == roll[4]
	) and not is_yahtzee(*roll)

def _is_three(*roll):
	return (
		roll[0] == roll[1] == roll[2] or
		roll[0] == roll[1] == roll[3] or
		roll[0] == roll[1] == roll[4] or
		roll[0] == roll[2] == roll[3] or
		roll[0] == roll[2] == roll[4] or
		roll[0] == roll[3] == roll[4] or
		roll[1] == roll[2] == roll[3] or
		roll[1] == roll[2] == roll[4] or
		roll[1] == roll[3] == roll[4] or
		roll[2] == roll[3] == roll[4]
	) and not is_four(*roll) and not is_yahtzee(*roll)

def is_three(*roll):
	return _is_three(*roll) and not full_house(*roll)

def long_straight(*roll):
	s = sorted(list(set(roll)))
	if len(s) < 5: return False
	return s[0] + 4 == s[1] + 3 == s[2] + 2 == s[3] + 1 == s[4]

def short_straight(*roll):
	s = sorted(list(set(roll)))
	if len(s) == 5:
		return (s[0] + 3 == s[1] + 2 == s[2] + 1 == s[3] or
		s[1] + 3 == s[2] + 2 == s[1] + 1 == s[0]) and not long_straight(*roll)
	elif len(s) == 4:
		return s[0] + 3 == s[1] + 2 == s[2] + 1 == s[3]
	return False

def full_house(*roll):
	return len(set(roll)) == 2 and _is_three(*roll)

def two_pairs(*roll):
	return len(set(roll)) == 3 and not is_three(*roll)

def one_pair(*roll):
	return len(set(roll)) == 4 and not short_straight(*roll)

def ev(f):
	def temp(*x):
		v = f(*x)
		if v:
			return v
		return 0
	return temp

@ev
def ev_yahtzee(*roll):
	if is_yahtzee(*roll):
		return roll[0] * 5

@ev
def ev_four(*roll):
	if is_four(*roll):
		return sum(roll)

@ev
def ev_three(*roll):
	if is_three(*roll):
		return sum(roll)

@ev
def ev_full_house(*roll):
	if full_house(*roll):
		return 25

@ev
def ev_short_straight(*roll):
	if short_straight(*roll):
		return 30

@ev
def ev_long_straight(*roll):
	if long_straight(*roll):
		return 40

@ev
def ev_two_pairs(*roll):
	if two_pairs(*roll):
		return sum(roll)

@ev
def ev_one_pair(*roll):
	if one_pair(*roll):
		for x in set(roll):
			if roll.count(x) == 2:
				return 2 * x

def permutation():
	l = [1, 1, 1, 1, 1]
	for _ in range(6**5):
		yield tuple(l)
		l[4] += 1
		if l[4] == 7:
			l[4] = 1
			l[3] += 1
		if l[3] == 7:
			l[3] = 1
			l[2] += 1
		if l[2] == 7:
			l[2] = 1
			l[1] += 1
		if l[1] == 7:
			l[1] = 1
			l[0] += 1

def yahtzee(n=1000000):
	yahtzee_count = 0
	four_count = 0
	three_count = 0
	ls_count = 0
	ss_count = 0
	fh_count = 0
	tp_count = 0
	op_count = 0
	none_count = 0
	for roll in permutation():
		y = 0
		if is_yahtzee(*roll):
			yahtzee_count += 1
			y += 1
		if is_four(*roll):
			four_count += 1
			y += 1
		if is_three(*roll):
			three_count += 1
			y += 1
		if long_straight(*roll):
			ls_count += 1
			y += 1
		if short_straight(*roll):
			ss_count += 1
			y += 1
		if full_house(*roll):
			fh_count += 1
			y += 1
		if two_pairs(*roll):
			tp_count += 1
			y += 1
		if one_pair(*roll):
			op_count += 1
			y += 1
		if not y:
			none_count += 1

	return {
		'yahtzee': yahtzee_count,
		'four': four_count,
		'three': three_count,
		'long straight': ls_count,
		'short straight': ss_count,
		'full house': fh_count,
		'two pairs': tp_count,
		'one pair': op_count,
		'nothing': none_count
	}

def yahtzee_ev(filter=lambda *roll: True):
	s = 0
	c = 0
	for roll in permutation():
		if filter(*roll):
			s += evaluate(*roll)
			c += 1
	return s / c

def all_freezes(*roll):
	for n in range(6):
		for comb in itertools.combinations(roll, n):
			if len(comb) == 0:
				yield (comb, lambda *_roll: True)
			elif len(comb) == 1:
				yield (comb, lambda *_roll: _roll[0] == comb[0])
			elif len(comb) == 2:
				yield (comb, lambda *_roll: _roll[0] == comb[0] and _roll[1] == comb[1])
			elif len(comb) == 3:
				yield (comb, lambda *_roll: _roll[0] == comb[0] and _roll[1] == comb[1] and _roll[2] == comb[2])
			elif len(comb) == 4:
				yield (comb, lambda *_roll: _roll[0] == comb[0] and _roll[1] == comb[1] and _roll[2] == comb[2]
					and _roll[3] == comb[3])
			elif len(comb) == 5:
				yield (comb, lambda *_roll: _roll[0] == comb[0] and _roll[1] == comb[1] and _roll[2] == comb[2]
					and _roll[3] == comb[3] and _roll[4] == comb[4])

def evaluate(*roll):
	if full_house(*roll) and 5 in set(roll) and 6 in set(roll):
		return sum(roll)
	else:
		return sum([
			ev_yahtzee(*roll),
			ev_four(*roll),
			ev_three(*roll),
			ev_full_house(*roll),
			ev_short_straight(*roll),
			ev_long_straight(*roll),
			ev_two_pairs(*roll),
			ev_one_pair(*roll)
		])

def best_reroll(*roll):
	current_ev = evaluate(*roll)
	all_choices = []
	for comb, freeze_function in all_freezes(*roll):
		all_choices.append((comb, yahtzee_ev(filter=freeze_function)))
	best = sorted(all_choices, key=lambda x: x[1])[-1]
	if best[1] > current_ev:
		return best
	return ('no reroll', current_ev)
