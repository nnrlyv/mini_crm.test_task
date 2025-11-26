from typing import Optional, List, Tuple
import random
from sqlalchemy.orm import Session
from app import models


def get_available_operators_for_source(db: Session, source_id: int) -> List[Tuple[models.Operator, int]]:
    weights = db.query(models.OperatorSourceWeight).filter(models.OperatorSourceWeight.source_id == source_id).all()
    result = []
    for w in weights:
        op = db.query(models.Operator).get(w.operator_id)
        if op is None:
            continue
        if not op.active:
            continue
        if op.current_load is None:
            op.current_load = 0
        if op.current_load < op.load_limit:
            result.append((op, w.weight))
    return result

def select_operator_by_weight(candidates: List[Tuple[models.Operator, int]]) -> Optional[models.Operator]:
    if not candidates:
        return None
    ops = [c[0] for c in candidates]
    weights = [max(0, int(c[1])) for c in candidates]
    if sum(weights) == 0:
        # if all weights zero, fallback to uniform random
        return random.choice(ops)
    selected = random.choices(ops, weights=weights, k=1)[0]
    return selected


def allocate_operator(db: Session, source_id: int) -> Optional[models.Operator]:
    candidates = get_available_operators_for_source(db, source_id)
    if not candidates:
        return None
    selected = select_operator_by_weight(candidates)
    if selected is None:
        return None

    selected.current_load = (selected.current_load or 0) + 1
    db.add(selected)
    db.flush()
    return selected
