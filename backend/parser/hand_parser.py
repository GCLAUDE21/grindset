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

    # 9. Board
    hand["board"] = parse_board(hand_text)

    # 10. Actions par rue
    streets = {}
    
    preflop_match = re.search(
        r'\*\*\* PRE-FLOP \*\*\*(.*?)(?:\*\*\* FLOP \*\*\*|\*\*\* SUMMARY \*\*\*)',
        hand_text, re.DOTALL
    )
    if preflop_match:
        streets["preflop"] = parse_street(preflop_match.group(1), HERO)
    
    flop_match = re.search(
        r'\*\*\* FLOP \*\*\*.*?\n(.*?)(?:\*\*\* TURN \*\*\*|\*\*\* SUMMARY \*\*\*)',
        hand_text, re.DOTALL
    )
    if flop_match:
        streets["flop"] = parse_street(flop_match.group(1), HERO)
    
    turn_match = re.search(
        r'\*\*\* TURN \*\*\*.*?\n(.*?)(?:\*\*\* RIVER \*\*\*|\*\*\* SUMMARY \*\*\*)',
        hand_text, re.DOTALL
    )
    if turn_match:
        streets["turn"] = parse_street(turn_match.group(1), HERO)
    
    river_match = re.search(
        r'\*\*\* RIVER \*\*\*.*?\n(.*?)(?:\*\*\* SHOW DOWN \*\*\*|\*\*\* SUMMARY \*\*\*)',
        hand_text, re.DOTALL
    )
    if river_match:
        streets["river"] = parse_street(river_match.group(1), HERO)
    
    hand["streets"] = streets

    # 11. Showdown
    hand["showdown"] = parse_showdown(hand_text)

    # 12. Adversaires
    hand["opponents"] = parse_opponents(hand_text, HERO)

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

def parse_street(street_text, hero):
    """Extrait toutes les actions d'une rue avec leurs montants."""
    actions = []
    
    # Pattern pour chaque action
    patterns = [
        (r'(\w+(?:\.\w+)*(?:_\w+)*) bets (\d+)', 'bet'),
        (r'(\w+(?:\.\w+)*(?:_\w+)*) calls (\d+)', 'call'),
        (r'(\w+(?:\.\w+)*(?:_\w+)*) raises \d+ to (\d+)', 'raise'),
        (r'(\w+(?:\.\w+)*(?:_\w+)*) checks', 'check'),
        (r'(\w+(?:\.\w+)*(?:_\w+)*) folds', 'fold'),
        (r'(\w+(?:\.\w+)*(?:_\w+)*) raises \d+ to \d+ and is all-in', 'allin'),
        (r'(\w+(?:\.\w+)*(?:_\w+)*) bets \d+ and is all-in', 'allin'),
        (r'(\w+(?:\.\w+)*(?:_\w+)*) calls \d+ and is all-in', 'allin'),
    ]
    
    for line in street_text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        for pattern, action_type in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                player = match.group(1)
                amount = int(match.group(2)) if len(match.groups()) > 1 else 0
                actions.append({
                    "player": player,
                    "is_hero": player.lower() == hero.lower(),
                    "action": action_type,
                    "amount": amount
                })
                break
    
    return actions


def parse_board(hand_text):
    """Extrait les cartes du board rue par rue."""
    board = {}
    
    flop_match = re.search(r'\*\*\* FLOP \*\*\* \[(.+?)\]', hand_text)
    if flop_match:
        board["flop"] = flop_match.group(1).split()
    
    turn_match = re.search(r'\*\*\* TURN \*\*\* \[.+?\]\[(.+?)\]', hand_text)
    if turn_match:
        board["turn"] = turn_match.group(1).split()
    
    river_match = re.search(r'\*\*\* RIVER \*\*\* \[.+?\]\[(.+?)\]', hand_text)
    if river_match:
        board["river"] = river_match.group(1).split()
    
    return board


def parse_showdown(hand_text):
    """Extrait les cartes de tous les joueurs au showdown."""
    showdown = {}
    
    for match in re.finditer(r'(\w+(?:\.\w+)*(?:_\w+)*) shows \[(.+?)\]', hand_text, re.IGNORECASE):
        player = match.group(1)
        cards = match.group(2).split()
        showdown[player] = cards
    
    return showdown


def parse_opponents(hand_text, hero):
    """Extrait les infos de tous les adversaires."""
    opponents = []
    
    for match in re.finditer(r'Seat \d+: (\w+(?:\.\w+)*(?:_\w+)*) \((\d+)\)', hand_text):
        name = match.group(1)
        stack = int(match.group(2))
        if name.lower() != hero.lower():
            opponents.append({
                "name": name,
                "stack": stack
            })
    
    return opponents