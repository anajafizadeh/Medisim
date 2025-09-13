import yaml
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ParsedCase:
    meta: Dict[str, Any]
    reveals: Dict[str, str]
    orders_allowed: list
    order_results: Dict[str, str]
    expected: Dict[str, Any]


def parse_case_yaml(blob: str) -> ParsedCase:
    data = yaml.safe_load(blob)
    reveals = data.get('qa_reveals', {})
    orders = data.get('orders', {})
    return ParsedCase(
        meta={k: data.get(k) for k in ['id','title','specialty','difficulty','objectives','patient']},
        reveals=reveals,
        orders_allowed=orders.get('allowed', []),
        order_results=orders.get('results', {}),
        expected=data.get('expected', {}),
    )