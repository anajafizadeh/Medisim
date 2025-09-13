from typing import List

# Simple keyword → tag mapping for MVP; replace with LLM classification later
KEYWORD_TAGS = [
    ('when', 'hx_onset'),
    ('start', 'hx_onset'),
    ('burn', 'hx_quality'),
    ('discharge', 'hx_discharge'),
    ('flank', 'hx_flank_pain'),
    ('pregnan', 'hx_pregnancy'),
]

def classify_intents(message: str) -> List[str]:
    text = message.lower()
    tags = set()
    for kw, tag in KEYWORD_TAGS:
        if kw in text:
            tags.add(tag)
    return list(tags) or ['misc']