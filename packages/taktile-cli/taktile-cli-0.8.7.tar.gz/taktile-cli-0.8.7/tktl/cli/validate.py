import click

from tktl.cli.common import (
    ClickGroup,
    get_secrets,
    validate_integration_shared_options,
    validate_project_shared_options,
)
from tktl.commands.validate import (
    validate_all,
    validate_endpoint_sample,
    validate_import,
    validate_integration,
    validate_profiling,
    validate_project_config,
    validate_unittest,
)
from tktl.core.config import settings


@click.group(
    "validate", help="Validate the project", cls=ClickGroup, **settings.HELP_COLORS_DICT
)
def validate():
    pass


@validate.command("config", help="Validate the configuration")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
def validate_config_command(path) -> None:
    """Validates a new project for the necessary scaffolding, as well as the supporting
    files needed. The directory structure of a new project.
    """
    validate_project_config(path=path)


@validate.command("import", help="Validate src/endpoints.py")
@validate_project_shared_options
@click.option(
    "--secrets-repository",
    "-s",
    help="Full repository name (owner/name) to use from which to get the secret names",
    required=False,
)
def validate_import_command(
    path: str, cache: bool, prune: bool, secrets_repository: str
) -> None:
    secrets = get_secrets(secrets_repository)
    validate_import(path=path, cache=cache, prune=prune, secrets=secrets)


@validate.command("sample", help="Validate Sample Data on Endpoints")
@validate_project_shared_options
@click.option(
    "--secrets-repository",
    "-s",
    help="Full repository name (owner/name) to use from which to get the secret names",
    required=False,
)
def validate_sample_command(
    path: str, cache: bool, prune: bool, secrets_repository: str
) -> None:
    secrets = get_secrets(secrets_repository)
    validate_endpoint_sample(path=path, cache=cache, prune=prune, secrets=secrets)


@validate.command("unittest", help="Validate the unittests")
@validate_project_shared_options
@click.option(
    "--secrets-repository",
    "-s",
    help="Full repository name (owner/name) to use from which to get the secret names",
    required=False,
)
def validate_unittest_command(
    path: str, cache: bool, prune: bool, secrets_repository: str
) -> None:
    secrets = get_secrets(secrets_repository)
    validate_unittest(path=path, cache=cache, prune=prune, secrets=secrets)


@validate.command("integration", help="Validate integration")
@validate_integration_shared_options
@validate_project_shared_options
@click.option(
    "--secrets-repository",
    "-s",
    help="Full repository name (owner/name) to use from which to get the secret names",
    required=False,
)
def validate_integration_command(
    path: str,
    cache: bool,
    prune: bool,
    timeout: int,
    retries: int,
    secrets_repository: str,
) -> None:
    secrets = get_secrets(secrets_repository)
    validate_integration(
        path=path,
        cache=cache,
        prune=prune,
        timeout=timeout,
        retries=retries,
        secrets=secrets,
    )


@validate.command("profiling", help="Validate profiling")
@validate_integration_shared_options
@validate_project_shared_options
@click.option(
    "--secrets-repository",
    "-s",
    help="Full repository name (owner/name) to use from which to get the secret names",
    required=False,
)
def validate_profiling_command(
    path: str,
    cache: bool,
    prune: bool,
    timeout: int,
    retries: int,
    secrets_repository: str,
) -> None:
    secrets = get_secrets(secrets_repository)
    validate_profiling(
        path=path,
        cache=cache,
        prune=prune,
        timeout=timeout,
        retries=retries,
        secrets=secrets,
    )


@validate.command("all", help="Validate everything")
@validate_integration_shared_options
@validate_project_shared_options
@click.option(
    "--secrets-repository",
    "-s",
    help="Full repository name (owner/name) to use from which to get the secret names",
    required=False,
)
def validate_all_command(
    path: str,
    cache: bool,
    prune: bool,
    timeout: int,
    retries: int,
    secrets_repository: str,
) -> None:
    secrets = get_secrets(secrets_repository)
    validate_all(
        path=path,
        cache=cache,
        prune=prune,
        timeout=timeout,
        retries=retries,
        secrets=secrets,
    )
