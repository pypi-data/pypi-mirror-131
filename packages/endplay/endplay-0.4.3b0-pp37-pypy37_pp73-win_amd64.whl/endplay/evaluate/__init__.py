"""
Functions for evaluating bridge hands using a variety of different metrics.
"""

from __future__ import annotations

__all__ = [
	"hcp", "top_honours", "losers", "cccc", "quality", "controls", "rule_of_n",
	"exact_shape", "shape", "major_shape", "minor_shape", "is_balanced",
	"is_semibalanced", "is_minor_semibalanced", "is_single_suited", "is_two_suited",
	"is_three_suited"]

from typing import Union
from collections.abc import Iterable
from endplay.types import *

standard_hcp_scale = { Rank.RA: 4, Rank.RK: 3, Rank.RQ: 2, Rank.RJ: 1}
bergen_hcp_scale = { Rank.RA: 4.5, Rank.RK: 3, Rank.RQ: 1.5, Rank.RJ: 0.75, Rank.RT: 0.25}

def hcp(obj: Union[Hand, SuitHolding, Card, Rank], scale: dict[Rank, int] = standard_hcp_scale) -> float:
	"Return the hcp value of a card or rank, or calculate the total of a holding or hand"
	if isinstance(obj, Rank):
		return scale[obj] if obj in scale else 0
	# Recursively call until we have a rank
	if isinstance(obj, Card):
		return hcp(obj.rank, scale)
	else:
		return sum(hcp(card, scale) for card in obj)

def top_honours(hand: Union[Hand, SuitHolding], lowest_honour: Union[Rank, int] = Rank.RJ) -> int:
	"""
	Return the number of top honors in a suit

	:param suit: The suit holding to evaluate
	:param lowest_honour: The lowest rank to be treated as an honour, or an
		integer for how many top cards are honours
	"""
	if not isinstance(lowest_honour, Rank):
		lowest_honour = AlternateRank(15 - lowest_honour).to_standard()
	if isinstance(hand, SuitHolding):
		return sum(1 for rank in hand if rank >= lowest_honour)
	else:
		return sum(1 for card in hand if card.rank >= lowest_honour)

def losers(hand: Union[Hand, SuitHolding]) -> int:
	"""
	Returns the number of losers in a hand. The number of losers in each
	suit is calculated as: (a) 3 or more cards in a suit: 3 - 1 per AKQ
	(b) Doubleton: AK=0, Ax/Kx=1, else 2 (c) Singleton: A=0, else 1 (d) Void: 0
	"""
	if isinstance(hand, SuitHolding):
		a, k, q = Rank.RA in hand, Rank.RK in hand, Rank.RQ in hand
		if len(hand) == 0: return 0
		if len(hand) == 1: return 1 - a
		if len(hand) == 2: return 2 - a - k
		return 3 - a - k - q
	else:
		return sum(losers(hand[suit]) for suit in Denom.suits())

def cccc(hand: Union[Hand, SuitHolding]) -> float:
	"""
	Uses the Kaplan four cs algorithm from the October 1982 issue of Bridge world
	magazine. This implementation is based on the interpretation of the algorithm
	described on http://www.rpbridge.net/8j19.htm
	"""
	if isinstance(hand, Hand):
		return sum(cccc(hand[suit]) for suit in Denom.suits())
	l = len(hand)
	score = 0
	# 1-5: Count point values A=4,K=3,Q=2,J=1,T=0.5
	if Rank.RA in hand: score += 4
	if Rank.RK in hand: score += 3
	if Rank.RQ in hand: score += 2
	if Rank.RJ in hand: score += 1
	if Rank.RT in hand: score += 0.5
	# 6-7: if between 2-6 cards, count points for supported T and 9
	if l >= 2 and l <= 6:
		if (Rank.RT in hand) and ((Rank.RJ in hand) or top_honours(hand, 4) >= 2):
			score += 0.5
		if (Rank.R9 in hand) and ((Rank.R8 in hand or Rank.RT in hand) or top_honours(hand, 5) == 2):
			score += 0.5
	# 8: if between 4-6 cards, count 9 without any touching cards and exactly three higher honours
	if l >= 4 and l <= 6:
		if (Rank.R9 in hand) and not (Rank.R8 in hand and Rank.RT in hand) and top_honours(hand, 4) == 3:
			score += 0.5
	# 9: 7+ cards missing queen or jack (or both)
	if l >= 7 and (Rank.RQ not in hand or Rank.RJ not in hand):
		score += 1
	# 10: 8+ cards missing queen
	if l >= 8 and Rank.RQ not in hand:
		score += 1
	# 11: 9+ cards missing queen and jack
	if l >= 9 and (Rank.RQ not in hand and Rank.RJ not in hand):
		score += 1
	# 12: Multiply current total by suit length, divide by 10, then continue
	score *= l / 10
	# 13: Add 3 for an ace
	if Rank.RA in hand:
		score += 3
	# 14-15: Add 2 for guarded king and 0.5 for king singleton
	if Rank.RK in hand:
		if l > 1: score += 2
		else: score += 0.5
	# 16-19: Add values for queen
	if Rank.RQ in hand:
		if l >= 3:
			# 16-17: 3+ cards, +1 if has higher honour else +0.75
			if Rank.RK in hand or Rank.RA in hand:
				score += 1
			else:
				score += 0.75
		elif l == 2:
			# 18-19: doubleton, +0.5 if has higher honour else +0.25
			if Rank.RK in hand or Rank.RA in hand:
				score += 0.5
			else:
				score += 0.25
	# 20-21: Jack with two higher honours=0.5, one higher honour=0.25
	if Rank.RJ in hand:
		hh = top_honours(hand, 3)
		if hh == 2:
			score += 0.5
		elif hh == 1:
			score += 0.25
	# 22-23: Ten with two higher honours=0.25, T9 with one higher honour=0.25
	if Rank.RT in hand:
		hh = top_honours(hand, 4)
		if hh == 2:
			score += 0.25
		if Rank.R9 in hand and hh == 1:
			score += 0.25
	# 24-26: void=3, singleton=2, doubleton=1
	if l == 0:
		score += 3
	elif l == 1:
		score += 2
	elif l == 2:
		score += 1
	return score

def quality(hand: SuitHolding) -> float:
	"Uses the quality algorithm (from the October 1982 issue of Bridge World magazine"
	raise NotImplementedError

def controls(hand: Union[Iterable, Card, Rank]) -> int:
	"Return the number of controls in a sequence, using A=2 and K=1"
	if isinstance(hand, Rank):
		if hand == Rank.RA: return 2
		elif hand == Rank.RK: return 1
		else: return 0
	elif isinstance(hand, Card):
		return controls(hand.rank)
	else:
		return sum(controls(card) for card in hand)

def rule_of_n(hand: Hand) -> int:
	"Returns the hcp of the hand added to the length of the two longest suits"
	s = shape(hand)
	return hcp(hand) + s[0] + s[1]

def exact_shape(hand: Hand) -> list[int]:
	"Return the shape of a hand as a list starting from spades, e.g. (5, 2, 3, 3)"
	return [len(hand[suit]) for suit in Denom.suits()]

def shape(hand: Hand) -> list[int]:
	"""
	Return the shape of a hand as a list from longest to shortest, e.g. a 3424 would
	return (4, 4, 3, 2)
	"""
	return sorted(exact_shape(hand), reverse=True)

def major_shape(hand: Hand) -> list[int]:
	"Return the shape of a hand's major holding from longest to shortest"
	return sorted((len(hand[Denom.spades]), len(hand[Denom.hearts])), reverse=True)

def minor_shape(hand: Hand) -> list[int]:
	"""
	Return the shape of a hand's minor holding from longest to shortest
	"""
	return sorted((len(hand[Denom.diamonds]), len(hand[Denom.clubs])), reverse=True)

def is_balanced(hand: Hand) -> bool:
	"""
	Returns True if the hand shape is 4333, 4432 or 5332
	"""
	s = shape(hand)
	return s in ([4,3,3,3],[4,4,3,2],[5,3,3,2])

def is_semibalanced(hand: Hand) -> bool:
	"""
	Returns True if the hand shape is balanced or 5422
	"""
	s = shape(hand)
	return is_balanced(hand) or s == [5, 4, 2, 2]

def is_minor_semibalanced(hand: Hand) -> bool:
	"""
	Returns True if the hand shape is balanced or contains 
	doubletons in both minors
	"""
	return is_balanced(hand) or minor_shape(hand) == [2, 2]

def is_single_suited(hand: Hand, min_length: int = 6, no_side_suit: bool = False) -> bool:
	"""
	Returns True if the hand is singled suited

	:param min_length: The minimum number of cards to hold in the suit
	:param no_side_suit: If True, the hand cannot contain another 4 card suit
	"""
	s = shape(hand)
	if no_side_suit:
		return s[0] >= min_length and s[1] < 4
	else:
		return s[0] >= min_length

def is_two_suited(hand: Hand, strict: bool = False) -> bool:
	"""
	Returns True if the hand contains at least 10 cards in two suits.

	:param strict: Hand must be at least 5-5
	"""
	s = shape(hand)
	if strict:
		return s[0] + s[1] >= 10 and s[1] >= 5
	else:
		return s[0] + s[1] >= 10

def is_three_suited(hand: Hand, strict: bool = False) -> bool:
	"""
	Returns True if the hand has three suits with at least four cards in them.

	:param strict: Only return true if the hand is 4441
	"""
	s = shape(hand)
	if strict:
		return s == [4, 4, 4, 1]
	else:
		return s[0] >= 4 and s[1] >= 4 and s[2] >= 4