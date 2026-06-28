import re
from hand_parser import parse_file

filepath = "/Users/guillaumeclaude/Library/Application Support/winamax/documents/accounts/piiicka/history/20260628_Expresso(1138591464)_real_holdem_no-limit.txt"

hands = parse_file(filepath)

print(f"Nombre de mains parsées : {len(hands)}")
for hand in hands:
    print(hand)

for hand in hands:
    if "hero_preflop_action" not in hand:
        print(f"\nMAIN SANS ACTION: {hand['hand_id']}")
        print(f"Cartes: {hand.get('hero_cards')}")