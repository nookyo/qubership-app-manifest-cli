import sys, typer, json
from ..ops.components import add_component as _add_component
from ..ops.dependencies import add_dependency as _add_dependency

def add_command(
    manifest: str = typer.Argument(...),
    section: str = typer.Argument(...),
    text: str | None = typer.Option(None, "--text"),
    file: typer.FileText | None = typer.Option(None, "--file", "-f"),
    configuration: str | None = typer.Option(None, "--config", "-c"),
    out: typer.FileTextWrite | None = typer.Option(None, "--out", "-o"),
):
    payload_text = file.read() if file else (text if text is not None else sys.stdin.read())
    if section == "components":
        _add_component(manifest, payload_text, out)
    elif section == "dependencies":
        _add_dependency(manifest, payload_text, configuration, out)
    else:
        raise typer.BadParameter("section must be 'components' or 'dependencies'")
