from typing import List, Any, Dict


def field_analyzer(models: List[Dict[str, Any]]):
    props = {}
    for m in models:
        for k, v in m.items():
            props[k] = type(v)

    for k, v in props.items():
        print(f"{k}: {v.__name__}")
