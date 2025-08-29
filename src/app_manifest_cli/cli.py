import typer
from .commands.add import add_command
from .commands.create import create_command
from .commands.generate import generate_command

app = typer.Typer()
app.command("create")(create_command)
app.command("add")(add_command)
app.command("generate")(generate_command)
# Example command:
# $env:PYTHONPATH="src"
# python -m app_manifest_cli.cli generate -o manifest.json --name test-application --version 1.0.0 --config ./example/metadata-deps.yaml ./example/patroni-core.json ./example/patroni-services.json ./example/qubership-logging-integration-tests-main-7d429a4d37e2.json
if __name__ == "__main__":
    app()
