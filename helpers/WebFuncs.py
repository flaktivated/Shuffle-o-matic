__version__ = '0.1.0'

import os
from helpers.Gameplay import *

CMD_FILE = '/var/www/html/data.txt'
# CMD_FILE = 'data.txt'
SHUFFLES = ['RAND', 'BJACK', 'HOLD']

def check_for_cmd():
    """ Returns tuple of [Type] [Data] where type is the shuffle type and data
    will contain either random shuffle parameters or the top deck order required """
    try:
        with open(CMD_FILE, 'r+') as f:
            data = f.readline()
            f.truncate(0)

        rawdata = data.split(',')
        if rawdata[0] in SHUFFLES:
            shuffletype = SHUFFLES.index(rawdata[0])
            if shuffletype is 0:
                return (rawdata[0], format_rand(rawdata[1:]))
            elif shuffletype is 1:
                return (rawdata[0], format_bjack(rawdata[1:]))
            elif shuffletype is 2:
                return (rawdata[0], format_holdem(rawdata[1:]))

    except:
        pass
    
    return (None, None)

def format_rand(data):
    return [int(i) for i in data]

def format_bjack(data):
    # Gather data
    n_players = int(data[0])
    def wincheck(val):
        if "true" in val:
            return True
        return False
    winner = [wincheck(i) for i in data[1:]]

    # Build desired deck based on winners
    deck = BlackJack(n_players=n_players)
    for i, w in enumerate(winner):
        if i < n_players:
            hand = CardSet()
            if w is True:
                hand.add_card(rank='A')
                hand.add_card(rank=['K', 'Q', 'J', '10'])
            else:
                hand.add_card(rank=['2', '3', '4', '5', '6', '7', '8', '9'])
                hand.add_card(rank=['2', '3', '4', '5', '6', '7', '8', '9'])
            deck.add_card_set(hand)

    deck.generate_deck()
    return deck

def format_holdem(data):
    # Gather data
    n_players = int(data[0])
    discard_between_flops = "true" in data[1]

    # Build desired deck and list of all cards. Any used will be removed (for discards)
    deck = Holdem(n_players=n_players)
    discards = CardSet()
    discards.add_card(rank=ALLRANKS, suit=ALLSUITS)
    hands = [CardSet()] * (n_players + 3)

    # Fill out hands prioritizing fully defined cards, then rank only, then suit only
    cards_in_set = [3,1,1,2,2,2,2,2,2,2,2]
    set_i = 0
    i = 0
    while i < sum(cards_in_set):
        for _ in range(cards_in_set[set_i]):
            rank = data[i]
            suit = data[i + 1]
            if rank is not "" and suit is not "":
                hands[set_i].add_card(rank=rank, suit=suit)
                discards.remove_card(Card(rank=rank, suit=suit))
            i += 1
        set_i += 1

    set_i = 0
    i = 0
    while i < sum(cards_in_set):
        for _ in range(cards_in_set[set_i]):
            rank = data[i]
            suit = data[i + 1]
            if rank is not "" and suit is "":
                cards_to_add = discards.get_cards_not_in_set(rank=rank)
                hands[set_i].add_card(specific_cards=cards_to_add)
                for c in cards_to_add:
                    discards.remove_card(c)
            i += 1
        set_i += 1

    set_i = 0
    i = 0
    while i < sum(cards_in_set):
        for _ in range(cards_in_set[set_i]):
            rank = data[i]
            suit = data[i + 1]
            if rank is "" and suit is not "":
                cards_to_add = discards.get_cards_not_in_set(suit=suit)
                hands[set_i].add_card(specific_cards=cards_to_add)
                for c in cards_to_add:
                    discards.remove_card(c)
            i += 1
        set_i += 1

    set_i = 0
    i = 0
    while i < sum(cards_in_set):
        for _ in range(cards_in_set[set_i]):
            rank = data[i]
            suit = data[i + 1]
            if rank is "" and suit is "":
                hands[set_i].add_card(discards.cards[0])
            i += 1
        set_i += 1

    deck.generate_deck(discard_between=discard_between_flops)
    return deck

if __name__=='__main__':
    cmd, deck = check_for_cmd()
    deck.break_into_bins(8)
    print(deck.deck_order)
    print(deck.bin_order)
    print(deck.card_sets)
    print(deck.bin_dispense_index)

    two = Card(rank='2', suit='D')
    ace = Card(rank='A', suit='D')
    ten = Card(rank='10', suit='D')

    for i in range(3):
        print('two: ', deck.get_bin(two))
        print(deck.bin_dispense_index, '\n')
        print('ace: ', deck.get_bin(ace))
        print(deck.bin_dispense_index, '\n')
        print('ten: ', deck.get_bin(ten))
        print(deck.bin_dispense_index, '\n')
        print(deck.is_shuffle_complete())
        print('\n\n')
