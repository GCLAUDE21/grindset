import re

HERO = "piiicka"

def parse_hand(hand_text):
    hand = {}

    # 1. Hand ID
    id_match = re.search(r'HandId: #(\S+)', hand_text)
    if id_match:
        hand["hand_id"] = id_match.group(1)

    # 2. Buy-in
    buyin_match = re.search(r'buyIn: ([\d.]+)€', hand_text)
    if buyin_match:
        hand["buy_in"] = float(buyin_match.group(1))

    # 3. Blinds
    blinds_match = re.search(r'no limit \((\d+)/(\d+)\)', hand_text)
    if blinds_match:
        hand["small_blind"] = int(blinds_match.group(1))
        hand["big_blind"] = int(blinds_match.group(2))

    # 4. Cartes du hero
    cards_match = re.search(r'Dealt to ' + HERO + r' \[(.+?)\]',
                            hand_text, re.IGNORECASE)
    if cards_match:
        hand["hero_cards"] = cards_match.group(1).split()

    # 5. Stack du hero au début de la main
    stack_match = re.search(HERO + r' \((\d+)\)', hand_text, re.IGNORECASE)
    if stack_match:
        hand["hero_stack"] = int(stack_match.group(1))

        # 5b. Stack en big blinds
    if "hero_stack" in hand and "big_blind" in hand:
        hand["hero_stack_bb"] = round(hand["hero_stack"] / hand["big_blind"], 1)

    # 6. Position du hero
    button_match = re.search(r'Seat #(\d+) is the button', hand_text)
    seat_match = re.search(r'Seat (\d+): ' + HERO, hand_text, re.IGNORECASE)
    if button_match and seat_match:
        button_seat = int(button_match.group(1))
        hero_seat = int(seat_match.group(1))
        if hero_seat == button_seat:
            hand["hero_position"] = "BTN"
        elif hero_seat == button_seat % 3 + 1:
            hand["hero_position"] = "SB"
        else:
            hand["hero_position"] = "BB"

    # 7. Action du hero pre-flop
    preflop_match = re.search(
        r'\*\*\* PRE-FLOP \*\*\*(.*?)(?:\*\*\* FLOP \*\*\*|\*\*\* SUMMARY \*\*\*)',
        hand_text, re.DOTALL
    )
    if preflop_match:
        preflop = preflop_match.group(1)
        if re.search(HERO + r'.*?and is all-in', preflop, re.IGNORECASE):
            hand["hero_preflop_action"] = "allin"
        elif re.search(HERO + r'.*?folds', preflop, re.IGNORECASE):
            hand["hero_preflop_action"] = "fold"
        elif re.search(HERO + r'.*?raises', preflop, re.IGNORECASE):
            hand["hero_preflop_action"] = "raise"
        elif re.search(HERO + r'.*?calls', preflop, re.IGNORECASE):
            hand["hero_preflop_action"] = "call"
        elif re.search(HERO + r'.*?checks', preflop, re.IGNORECASE):
            hand["hero_preflop_action"] = "check"
        else:
            hand["hero_preflop_action"] = "check"

    # 8. Est-ce que le hero a gagné ?
    won_match = re.search(HERO + r'.*?won (\d+)', hand_text, re.IGNORECASE)
    if won_match:
        hand["hero_won"] = True
        hand["hero_chips_won"] = int(won_match.group(1))
    else:
        hand["hero_won"] = False
        hand["hero_chips_won"] = 0

    return hand

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Découper en mains individuelles
    hands_raw = content.strip().split('\n\n\n')

    # Parser chaque main
    hands = []
    for hand_text in hands_raw:
        if 'HandId' in hand_text:
            parsed = parse_hand(hand_text)
            if parsed:
                hands.append(parsed)

    return hands