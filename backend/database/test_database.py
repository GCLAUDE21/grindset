import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.database.database import init_db, save_hands, get_all_hands
from backend.parser.hand_parser import parse_file

filepath = "/Users/guillaumeclaude/Library/Application Support/winamax/documents/accounts/piiicka/history/20260628_Expresso(1138591464)_real_holdem_no-limit.txt"

init_db()

hands = parse_file(filepath)
print(f"Mains parsées : {len(hands)}")

save_hands(hands)

all_hands = get_all_hands()
print(f"Mains en base : {len(all_hands)}")
print(f"Première main : {all_hands[0]}")