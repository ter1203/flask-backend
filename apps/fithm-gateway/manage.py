from flask.cli import AppGroup
import click
from main import app
from libs.database import create_tables

db_cli = AppGroup('db')

@db_cli.command('create')
def create_db():
    create_tables()

app.cli.add_command(db_cli)
