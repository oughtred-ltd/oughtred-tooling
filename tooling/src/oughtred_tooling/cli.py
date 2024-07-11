import os
import pprint
import click
from oughtred_tooling.al_parser import process_directory, query_apis
import toml

@click.group()
def cli():
    pass

@cli.group("api")
def _group_api():
    pass

@_group_api.command("parse")
@click.argument('directory')
@click.option("--save", "-s", default=None)
@click.option("--append", "-a", default=False)
@click.option("--print", "-p", default=False)
def parse_api(directory, save, append, print):
    res = process_directory(directory, print)

    if not save:
        return
    
    if append:
        with open(save, 'r') as f:
            existing = toml.load(f)
            existing.update(res)
    else:
        existing = res

    with open(save, 'w') as f:
        toml.dump(existing, f)

@_group_api.command("lookup")
@click.argument('query')
@click.option("--only-fields", "-f", default=False)
def lookup_api(query, only_fields):
    if not os.path.exists("API_ENDPOINTS.toml"):
        raise click.ClickException("API_ENDPOINTS.toml not found.")

    for table, details in query_apis(query):
        if only_fields:
            for field in details['fields']:
                print(f"{field['name']}")
        else:
            print(table)
            pprint.pprint(details)

if __name__ == "__main__":
    cli()