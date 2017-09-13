from elbotto.card import Color, Card, CARD_OFFSET, CARDS_PER_COLOR

import pytest

def test_from_idx():
    for color in Color:
        for number in range(CARD_OFFSET, CARD_OFFSET + CARDS_PER_COLOR):
            card = Card.create(number, color.name)
            idx_card = Card.form_idx(card.id)

            assert card == idx_card

