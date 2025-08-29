import typer
from .commands.add import add_command
from .commands.create import create_command

app = typer.Typer()
app.command("create")(create_command)
app.command("add")(add_command)

if __name__ == "__main__":
    app()
