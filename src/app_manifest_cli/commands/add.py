import sys, typer, json
from ..services.components import add_component as _add_component
from ..services.dependencies import add_dependency as _add_dependency

def add_command(
    manifest: str = typer.Argument(...),
    section: str = typer.Argument(...),
    text: str | None = typer.Option(None, "--text"),
    file: typer.FileText | None = typer.Option(None, "--file", "-f"),
    configuration: str | None = typer.Option(None, "--config", "-c"),
    out: typer.FileTextWrite | None = typer.Option(None, "--out", "-o"),
):

    if section == "components":
        payload_text = file.read() if file else (text if text is not None else sys.stdin.read())
        _add_component(manifest, payload_text, out)
    elif section == "dependencies":
        if configuration and (file or text):
            raise typer.BadParameter("Only one of --config or --file/--text can be provided for dependencies")
        if not configuration:
            payload_text = file.read() if file else (text if text is not None else sys.stdin.read())
            _add_dependency(manifest_path=manifest, payload_text=payload_text, configuration=None, out_file=out)
        else:
            _add_dependency(manifest_path=manifest, payload_text=None, configuration=configuration, out_file=out)
    else:
        raise typer.BadParameter("section must be 'components' or 'dependencies'")
