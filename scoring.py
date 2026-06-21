from questions import QUESTIONS, CATEGORIES

def calculate_personal_scores(answers_dict):
    scores = {}
    for cat in CATEGORIES:
        cat_questions = [q for q in QUESTIONS if q["category"] == cat]
        vals = [int(answers_dict.get(str(q["id"]), answers_dict.get(q["id"], 3))) for q in cat_questions]
        scores[cat] = round(sum(vals) / len(vals), 2) if vals else 0
    return scores

def compute_benchmark(vorarbeiter_rows):
    if not vorarbeiter_rows:
        return None
    sums = {cat: 0.0 for cat in CATEGORIES}
    counts = {cat: 0 for cat in CATEGORIES}
    import json
    for row in vorarbeiter_rows:
        answers = json.loads(row["answers"])
        scores = calculate_personal_scores(answers)
        for cat in CATEGORIES:
            sums[cat] += scores[cat]
            counts[cat] += 1
    return {cat: round(sums[cat] / counts[cat], 2) if counts[cat] else 0 for cat in CATEGORIES}

def compute_match(bewerber_scores, benchmark):
    if not benchmark:
        return None, None
    max_diff = 4.0  # 1-5 scale
    per_domain = {}
    for cat in CATEGORIES:
        diff = abs(bewerber_scores[cat] - benchmark[cat])
        pct = max(0, round((1 - diff / max_diff) * 100, 1))
        per_domain[cat] = pct
    overall = round(sum(per_domain.values()) / len(per_domain), 1)
    return overall, per_domain

def compute_euclidean_distance(bewerber_scores, benchmark):
    if not benchmark:
        return None
    import math
    squared_sum = sum((bewerber_scores[cat] - benchmark[cat]) ** 2 for cat in CATEGORIES)
    return round(math.sqrt(squared_sum), 2)

def compute_percentile_rank(value, all_values):
    if not all_values:
        return 50
    below = sum(1 for v in all_values if v < value)
    equal = sum(1 for v in all_values if v == value)
    return round((below + 0.5 * equal) / len(all_values) * 100, 1)
