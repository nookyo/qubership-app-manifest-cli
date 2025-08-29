import json, yaml, sys, typer
from ..commands.create import create_command
from ..commands.create import get_boom_ref
from ..services.components import add_component as _add_component
from ..services.dependencies import add_dependency as _add_dependency
from pathlib import Path
from typing import List
def generate_command(
    components_files: List[Path] = typer.Argument(
        ..., help="One or more file paths to process."
    ),
    configuration: str | None = typer.Option(None, "--config", "-c"),
    name: str = typer.Option(
        "qubership-integration-platform", "--name", help="Application name"
    ),
    version: str = typer.Option("1.2.3", "--version", help="Application version"),
    out: str | None = typer.Option(None, "--out", "-o", help="Output file (default: stdout)"),
) -> None:
    configuration_data = load_configuration(configuration)

    body = create_command(name=name, version=version, out=open(out, "w"))
    # Получаю компоненты из конфига -- именно они определяют состав манифеста
    config_components = configuration_data.get("components", [])
    # Получаю депенденси из конфига
    config_dependencies = configuration_data.get("dependencies", [])
    # Читаю все json файлы с компонентами
    json_components = []
    for json_path in components_files:
        with open(json_path.resolve(), "r", encoding="utf-8") as f:
            json_comp = json.load(f)
            json_components.append(json_comp)
    # Перебираю компоненты из конфига, если в json_components есть такой же, то обновляю его
    components = []
    for conf_comp in config_components:
        for json_comp in json_components:
            if conf_comp["name"] == json_comp["name"] and conf_comp["mime-type"] == json_comp["mime-type"]:
                conf_comp.update(json_comp)
        if "bom-ref" not in conf_comp:
            conf_comp["bom-ref"] = get_boom_ref(conf_comp["name"])
        components.append(conf_comp)
        _add_component(manifest_path=out, payload_text=json.dumps(conf_comp), out_file=None)
    components_list = [ comp["mime-type"] + ":" + comp["name"] for comp in components]
    for dep in config_dependencies:
        dep_record = {}
        if "ref" not in dep:
            raise ValueError("Each dependency must have a 'ref' field")
        if "dependsOn" not in dep:
            raise ValueError("Each dependency must have a 'dependsOn' field")
        if dep["ref"] not in components_list:
            raise ValueError(f"Dependency ref '{dep['ref']}' not found in components")
        dep_record["ref"] = next(comp for comp in components if (comp["mime-type"] + ":" + comp["name"]) == dep["ref"])["bom-ref"]
        dep_record["dependsOn"] = []
        for d in dep["dependsOn"]:
            if d not in components_list:
                raise ValueError(f"Dependency dependsOn '{d}' not found in components")
            depends_on_component = next(comp for comp in components if (comp["mime-type"] + ":" + comp["name"]) == d)
            dep_record["dependsOn"].append(depends_on_component["bom-ref"])
        _add_dependency(manifest_path=out, payload_text=json.dumps(dep_record), configuration=None, out_file=None)

def load_configuration(configuration: str) -> dict:
    # bomFormat: CycloneDX
    # specVersion: "1.6"
    # metadata:
    #   component:
    #   type: application
    #   mime-type: application/vnd.qubership.application
    #   name: qubership-integration-platform
    #   version: "1.0.0"
    # tools:
    #   components:
    #   - type: application
    #     name: sbom-generator
    #     version: "2.3.1"

    with open(configuration, "r") as f:
        configuration_data = yaml.safe_load(f)
    if "components" not in configuration_data:
        raise ValueError("Configuration file must contain 'components' section")
    if "dependencies" not in configuration_data:
        raise ValueError("Configuration file must contain 'dependencies' section")
    return configuration_data

