import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from backend.agents.llm import get_llm
from backend.config import HERO

# 1. L'état de l'agent
class GTOState(TypedDict):
    hand: dict
    analysis: str
    score: int
    is_correct: bool

# 2. Le noeud d'analyse
def analyze_preflop(state: GTOState) -> GTOState:
    hand = state["hand"]
    llm = get_llm()

    hero_cards = json.loads(hand.get("hero_cards", "[]"))
    position = hand.get("hero_position", "")
    stack_bb = hand.get("hero_stack_bb", 0)
    action = hand.get("hero_preflop_action", "")
    big_blind = hand.get("big_blind", 20)

    streets = json.loads(hand.get("streets", "{}"))
    preflop_actions = streets.get("preflop", [])

    villain_action = "aucune action"
    for a in preflop_actions:
        if not a.get("is_hero"):
            villain_action = f"{a['action']} {a['amount']}" if a['amount'] > 0 else a['action']
            break

    prompt = f"""Tu es un coach poker expert en Expresso Winamax 3-max hyper-turbo.

Analyse cette situation preflop :
- Cartes : {' '.join(hero_cards)}
- Position : {position}
- Stack : {stack_bb} BB
- Action adverse : {villain_action}
- Decision hero : {action}

Reponds uniquement avec ce JSON sans apostrophes ni guillemets dans les valeurs texte :
{{"score": 75, "is_correct": true, "explanation": "explication ici", "gto_action": "allin"}}

Remplace les valeurs par ton analyse. Score entre 0 et 100. Pas de markdown."""

    response = llm.invoke(prompt)
    
    try:
        content = response.content.strip()
        
        # Nettoyer les balises markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        # Trouver le JSON entre les accolades
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end > start:
            content = content[start:end]
        
        result = json.loads(content.strip())
        
        return {
            **state,
            "analysis": result.get("explanation", ""),
            "score": result.get("score", 50),
            "is_correct": result.get("is_correct", True),
        }
    except Exception as e:
        # Si le JSON échoue, on parse manuellement le texte
        content = response.content
        score = 70
        is_correct = True
        
        if "incorrect" in content.lower() or "erreur" in content.lower() or "mauvais" in content.lower():
            is_correct = False
            score = 40
            
        return {
            **state,
            "analysis": content[:200],
            "score": score,
            "is_correct": is_correct,
        }

# 3. Construction du graphe
def build_gto_graph():
    graph = StateGraph(GTOState)
    graph.add_node("analyze", analyze_preflop)
    graph.set_entry_point("analyze")
    graph.add_edge("analyze", END)
    return graph.compile()

# 4. Fonction principale
def analyze_hand_gto(hand: dict) -> dict:
    graph = build_gto_graph()
    result = graph.invoke({"hand": hand})
    return {
        "score": result["score"],
        "is_correct": result["is_correct"],
        "analysis": result["analysis"]
    }