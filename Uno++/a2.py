#!/usr/bin/env python3
import random


class Card(object):

    """
    The basic type of colour and number.
    """

    def __init__(self, number, color):
        """
        The function structure of Card.

        :param number: card number
        :param color: card colour
        :param pickup: the amount of cards the next player should pickup, and the default is set to zero

        """
        self.number = number
        self.color = color
        # self.pickup_amount = pickup

    def __str__(self):
        return 'Card(%s, %s)' % (self.number, self.color)

    def __repr__(self):
        return self.__str__()

    def get_number(self):
        """

        :return: the card number
        """
        return self.number

    def get_colour(self):
        """

        :return:the card colour
        """
        return self.color

    def set_number(self, number: int):
        """

        :param number: set the number value of the card
        """
        self.number = number

    def set_colour(self, color: int):
        """

        :param color: Set the color of the card
        """
        self.color = color

    def get_pickup_amount(self):
        """

        :return: Returns the amount of cards the next player should pickup
        """
        return 0

    def matches(self, card):
        if self.number == card.get_number() and self.number != -1:
            return True
        elif self.color == card.get_colour():
            return True
        elif isinstance(self, Pickup4Card):
            return True
        elif isinstance(card, Pickup4Card):
            return True
        else:
            return False

    def play(self, player, game):
        pass


class SkipCard(Card):
    """
    A card which skips the turn of the next player. Matches with cards of the same colour.
    """
    def __init__(self, number, color):
        super(SkipCard, self).__init__(number, color)

    def __str__(self):
        return 'SkipCard(%s, %s)' % (self.number, self.color)

    def __repr__(self):
        return self.__str__()

    def play(self, player, game):
        """

        Perform a special card action to skip the player
        :param player: The current player
        :param game: Current game

        """
        game.skip()

    def matches(self, card):
        """
        rewrite matches method
        :param card: The card that compared with(to see if the user can play).
        :return: If the the card can be play the returns true, if not the result will return to false.

        """
        return self.get_colour() == card.get_colour()


class ReverseCard(Card):
    """
    A card which reverses the order of turns. Matches with cards of the same colour.
    """
    def __init__(self, number, color):
        super(ReverseCard, self).__init__(number, color)

    def __str__(self):
        return 'ReverseCard(%s, %s)' % (self.number, self.color)

    def __repr__(self):
        return self.__str__()

    def play(self, player, game):
        """

        Perform a special card action to reserve order of turns
        :param player: The current player
        :param game: Current game

        """
        game.reverse()

    def matches(self, card):
        """

        rewrite matches method
        :param card: The card that compared with(to see if the user can play).
        :return: If the the card can be play the returns true, if not the result will return to false.

        """
        return self.get_colour() == card.get_colour()


class Pickup2Card(Card):
    """
    A card which makes the next player pickup two cards. Matches with cards of the same colour
    """
    def __init__(self, number, color):
        super(Pickup2Card, self).__init__(number, color)
        # self.pickup_amount = 2

    def __str__(self):
        return 'Pickup2Card(%d, %s)' % (self.number, self.color)

    def __repr__(self):
        return self.__str__()

    def get_pickup_amount(self):
        """

        :return: Returns the amount of cards the next player should pickup
        """
        return 2

    def play(self, player, game):
        """

        Select the next player to choose 2 cards
        :param player: current player
        :param game: current game

        """
        game.get_turns().peak().get_deck().add_cards(game.pickup_pile.pick(2))


class Pickup4Card(Card):
    """
    A card which makes the next player pickup four cards. Matches with any card.
    """
    def __init__(self, number, color):
        super(Pickup4Card, self).__init__(number, color)

    def __str__(self):
        return 'Pickup4Card(%s, %s)' % (self.number, self.color)

    def __repr__(self):
        return self.__str__()

    def get_pickup_amount(self):
        """

        :return: Returns the amount of cards the next player should pickup
        """
        return 4

    def play(self, player, game):
        """

        Select the next player to choose 4 cards
        :param player: current player
        :param game: current game

        """

        game.get_turns().peak().get_deck().add_cards(game.pickup_pile.pick(4))


class Deck(object):
    """
    A collection of ordered Uno cards.
    """
    def __init__(self, starting_cards=None):
        self.cards = starting_cards or []

    def get_cards(self):
        """

        :return:Returns a list of cards in the deck.
        """
        return self.cards

    def get_amount(self):
        """

        :return:Returns the amount of cards in a deck.
        """
        return len(self.cards)

    def shuffle(self):
        """

        :return:Shuffle the order of the cards in the deck.
        """
        random.shuffle(self.cards)

    def pick(self, amount: int=1):
        """

        :param amount: Set the default == 1
        :return: Take the first 'amount' of cards off the deck and return them.
        """
        if amount < len(self.cards):
            pick_cards = list(self.cards[-amount:])
            self.cards = list(self.cards[:-amount])
        else:
            pick_cards = list(self.cards)
            self.cards = []
        return pick_cards

    def add_card(self, card):
        """
        Place a card on top of the deck.
        :param card: The card will be played

        """
        self.cards.append(card)

    def add_cards(self, cards=None):
        """
        Place a list of cards on top of the deck.
        :param cards: Saving updated lists for deck using.
        """
        if cards is None:
            cards = []
        self.cards.extend(cards)

    def top(self):
        """

        :return: Peaks at the card on top of the deck and returns it or None if the deck is empty.
        """
        return None if not len(self.cards) else self.cards[-1]


class Player(object):
    """
    A player represents one of the players in a game of uno.
    The basic type of computer player n human player.
    """
    def __init__(self, name):
        self.name = name
        self.deck = Deck()

    def get_name(self):
        """

        :return:Returns the name of the player.
        """
        return self.name

    def get_deck(self):
        """

        :return:Returns the players deck of cards.

        """
        return self.deck

    def is_playable(self):
        """

        :return:Returns True iff the players moves aren't automatic.
        """
        raise NotImplementedError

    def has_won(self):
        """

        :return: Returns True iff the player has an empty deck and has therefore won.

        """
        return len(self.get_deck().get_cards()) == 0

    def pick_card(self, putdown_pile: Deck):
        """
        Selects a card to play from the players current deck.
        :param putdown_pile:
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """
    A human player that selects cards to play using the GUI.

    """
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)

    def is_playable(self):
        return True

    def pick_card(self, putdown_pile: Deck):
        return None


class ComputerPlayer(Player):
    """
    A computer player that selects cards to play automatically.
    """
    def __init__(self, name):
        super(ComputerPlayer, self).__init__(name)

    def is_playable(self):
        return False

    def pick_card(self, putdown_pile: Deck):
        """

        :param putdown_pile:
        :return: Selects a card to play from the players current deck.
        """
        card = putdown_pile.top()
        select_card = None
        for select in self.get_deck().get_cards():
            if select.matches(card):
                self.get_deck().get_cards().remove(select)
                select_card = select
        return select_card


def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()

