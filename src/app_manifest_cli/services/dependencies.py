import json, yaml


def add_dependency(manifest_path: str, payload_text: str, configuration: str, out_file):

    # Тут можно написать логику для депенденси
    if not payload_text:
        if not configuration:
            raise ValueError("Either payload_text or configuration must be provided")
    if payload_text and configuration:
        raise ValueError("Only one of payload_text or configuration must be provided")

    if payload_text:
        payload_text = payload_text.strip()
        item = json.loads(payload_text)
        check_dependency(item)
        with open(manifest_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        m.setdefault("dependencies", []).append(item)
    else:
        with open(configuration, "r") as f:
            config_data = yaml.safe_load(f)
        if "dependencies" not in config_data:
            raise ValueError("Configuration file must contain 'dependencies' section")
        config_dependencies = config_data["dependencies"]
        with open(manifest_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        for dep in config_dependencies:
            check_dependency(dep)
            if dep["ref"] not in [(c["mime-type"] + ":" + c["name"]) for c in m.get("components", [])]:
                raise ValueError(f"Dependency ref '{dep['ref']}' not found in components")
            dep_record = {}
            dep_record["ref"] = next(c for c in m.get("components", []) if (c["mime-type"] + ":" + c["name"]) == dep["ref"])["bom-ref"]
            dep_record["dependsOn"] = []
            for d in dep["dependsOn"]:
                if d not in [(c["mime-type"] + ":" + c["name"]) for c in m.get("components", [])]:
                    raise ValueError(f"Dependency dependsOn '{d}' not found in components")
                dep_record["dependsOn"].append(next(c for c in m.get("components", []) if (c["mime-type"] + ":" + c["name"]) == d)["bom-ref"])

            m.setdefault("dependencies", []).append(dep_record)


    data = json.dumps(m, ensure_ascii=False, indent=2)
    if out_file:
        out_file.write(data)
    else:
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(data)

def check_dependency(dep: dict):
    if "ref" not in dep:
        raise ValueError("Dependency must have a 'ref' field")
    if "dependsOn" not in dep:
        raise ValueError("Dependency must have a 'dependsOn' field")
    if not isinstance(dep["dependsOn"], list):
        raise ValueError("Dependency 'dependsOn' field must be a list")
    return True
