from typing import Dict, Any

def evaluate_transcript(case: dict, messages: list, differential: list, final_dx: str, tests: list) -> Dict[str, Any]:
    # Minimal heuristic scorer for MVP
    expected = case.get('expected', {})
    must_dx = expected.get('differentials', {}).get('should_include', [])
    good_tests = case.get('orders', {}).get('allowed', [])

    asked_tags = set()
    for m in messages:
        for t in m.get('tags_json', []):
            asked_tags.add(t)

    hist_score = 2 if all(k in asked_tags for k in ['hx_onset','hx_discharge','hx_flank_pain','hx_pregnancy']) else (1 if any(k in asked_tags for k in ['hx_onset','hx_discharge']) else 0)
    diff_score = 2 if any(dx in must_dx for dx in differential+[final_dx]) else 1 if differential else 0
    test_score = 2 if any(t in good_tests for t in tests) else 0
    comm_score = 1  # placeholder

    scores = {
        'history_coverage': hist_score,
        'differential_quality': diff_score,
        'test_selection': test_score,
        'communication': comm_score,
    }
    overall = round((hist_score+diff_score+test_score+comm_score)/4, 2)

    feedback = {
        'history_coverage': 'Consider asking about pregnancy status and flank pain.' if hist_score<2 else 'Thorough history-taking.',
        'differential_quality': 'Include the most likely dx in your top 3.' if diff_score<2 else 'Good differential.',
        'test_selection': 'Urinalysis and pregnancy test are appropriate first-line tests.' if test_score<2 else 'Appropriate initial testing.',
        'communication': 'Try summarizing before moving on.'
    }
    return {'scores': scores, 'feedback': feedback, 'overall': overall}