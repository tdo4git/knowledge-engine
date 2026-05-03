import yaml
from pathlib import Path
from typing import Dict, Any


CONTRACT_DIR = Path(__file__).parent / "contracts"


# -------------------------------------------------
# Load by name (PRIMARY)
# -------------------------------------------------

def load_contract(name: str) -> Dict[str, Any]:

    path = CONTRACT_DIR / f"{name}.yaml"

    if not path.exists():
        raise FileNotFoundError(f"Contract not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -------------------------------------------------
# Load by role (for compatibility with MVP)
# -------------------------------------------------

def load_contract_by_role(role_name: str) -> Dict[str, Any]:

    mapping = {
        "Trusted Advisor": "advisor_regulatory_explanation",
        "Document Classifier": "classification"
    }

    contract_name = mapping.get(role_name)

    if not contract_name:
        raise ValueError(f"No contract defined for role: {role_name}")

    return load_contract(contract_name)


# -------------------------------------------------
# Load by task (NEW – preferred going forward)
# -------------------------------------------------

def load_contract_by_task(task_type: str) -> Dict[str, Any]:

    mapping = {
        "classification": "classification",
        "advisory": "advisor_regulatory_explanation"
    }

    contract_name = mapping.get(task_type)

    if not contract_name:
        raise ValueError(f"No contract defined for task: {task_type}")

    return load_contract(contract_name)