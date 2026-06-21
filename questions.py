CATEGORIES = {
    "Gewissenhaftigkeit & Sorgfalt": "conscientiousness",
    "Teamfähigkeit & Umgang": "teamwork",
    "Eigeninitiative & Verantwortung": "initiative",
    "Belastbarkeit & Einstellung": "resilience",
}

QUESTIONS = [
    {"id": 1,  "text": "Ich erledige meine Aufgaben stets termingerecht und vollständig.",                              "category": "Gewissenhaftigkeit & Sorgfalt"},
    {"id": 2,  "text": "Ich achte auf Details und mache meine Arbeit sauber und ordentlich.",                           "category": "Gewissenhaftigkeit & Sorgfalt"},
    {"id": 3,  "text": "Wenn ich etwas verspreche oder zusage, dann halte ich mich daran.",                            "category": "Gewissenhaftigkeit & Sorgfalt"},
    {"id": 4,  "text": "Ich bin morgens pünktlich und bereits vor Arbeitsbeginn einsatzbereit.",                       "category": "Gewissenhaftigkeit & Sorgfalt"},
    {"id": 5,  "text": "Ich arbeite gerne mit anderen zusammen und unterstütze Kollegen, wenn sie Hilfe brauchen.",    "category": "Teamfähigkeit & Umgang"},
    {"id": 6,  "text": "Kritik und Rückmeldungen kann ich annehmen, ohne gekränkt oder störrisch zu reagieren.",       "category": "Teamfähigkeit & Umgang"},
    {"id": 7,  "text": "Ich respektiere auch Kollegen, mit denen ich persönlich nicht gut auskomme.",                  "category": "Teamfähigkeit & Umgang"},
    {"id": 8,  "text": "Ich halte mich an Absprachen und Regeln – auch wenn niemand hinsieht.",                        "category": "Teamfähigkeit & Umgang"},
    {"id": 9,  "text": "Wenn ein Problem auftaucht, suche ich selbst nach einer Lösung, bevor ich Hilfe hole.",        "category": "Eigeninitiative & Verantwortung"},
    {"id": 10, "text": "Mir fallen Dinge auf, die verbessert werden könnten, und ich spreche sie an.",                "category": "Eigeninitiative & Verantwortung"},
    {"id": 11, "text": "Ich übernehme gerne Verantwortung für meine Aufgaben und entscheide eigenständig.",            "category": "Eigeninitiative & Verantwortung"},
    {"id": 12, "text": "Neue Dinge lerne ich schnell und frage nach, wenn mir etwas unklar ist.",                     "category": "Eigeninitiative & Verantwortung"},
    {"id": 13, "text": "Auch unter Druck oder Zeitstress bleibe ich ruhig und konzentriert.",                         "category": "Belastbarkeit & Einstellung"},
    {"id": 14, "text": "Rückschläge und Fehler stecke ich weg und mache motiviert weiter.",                           "category": "Belastbarkeit & Einstellung"},
    {"id": 15, "text": "Ich habe eine positive Grundeinstellung zur Arbeit und gebe auch bei eintönigen Aufgaben Gas.","category": "Belastbarkeit & Einstellung"},
]

LIKERT_LABELS = {
    1: "Trifft gar nicht zu",
    2: "Trifft eher nicht zu",
    3: "Teils / teils",
    4: "Trifft eher zu",
    5: "Trifft voll zu",
}

def get_category_short(cat):
    return CATEGORIES[cat]

def get_questions_by_category():
    result = {}
    for cat in CATEGORIES:
        result[cat] = [q for q in QUESTIONS if q["category"] == cat]
    return result
