# Beispiel für eine AI-Integration
def analyze_task(task):
    # Platzhalter für eine komplexere AI-Analyse
    # Könnte ein LLM aufrufen und die Task analysieren
    importance = "hoch" if "wichtig" in task['details'] else "niedrig"
    estimated_time = "1 Stunde" if "Präsentation" in task['details'] else "30 Minuten"
    return {'importance': importance, 'estimated_time': estimated_time}
