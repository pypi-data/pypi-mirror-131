import click
from supaconify.client import slack


@click.command()
@click.option("--slack-url")
def cli(slack_url):
    slack(slack_url)


if __name__ == "__main__":
    cli()
