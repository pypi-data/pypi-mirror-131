import os
import typing as t

from docker.errors import APIError  # type: ignore
from pydantic import ValidationError

from tktl.core.exceptions import (
    MissingDocker,
    NoContentsFoundException,
    UserRepoValidationException,
)
from tktl.core.loggers import LOG
from tktl.core.managers.docker import DockerManager
from tktl.core.managers.project import ProjectManager
from tktl.core.schemas.project import ProjectValidationOutput
from tktl.core.validation.outputs import (
    ConfigFileValidationFailure,
    ProjectValidationFailure,
)


def validate_project_config(path: str):
    try:
        LOG.log("=== VALIDATE PROJECT CONFIG STEP ===")
        ProjectManager.validate_project_config(path)
    except ValidationError as e:
        validation_output = ProjectValidationOutput(
            title=ConfigFileValidationFailure.title,
            summary=ConfigFileValidationFailure.summary,
            text=ConfigFileValidationFailure.format_step_results(validation_errors=e),
        )
        log_failure(validation_output)
        return
    except (NoContentsFoundException, UserRepoValidationException) as e:
        validation_output = ProjectValidationOutput(
            title=ProjectValidationFailure.title,
            summary=ProjectValidationFailure.summary,
            text=ProjectValidationFailure.format_step_results(validation_errors=e),
        )
        log_failure(validation_output)
        return
    LOG.log("Project scaffolding is valid!", color="green")


def log_failure(validation_output: ProjectValidationOutput):
    LOG.log(f"Project scaffolding is invalid: {validation_output.title}", color="red")
    LOG.log(validation_output.summary, color="red", err=True)
    LOG.log(validation_output.text, color="red", err=True)


def build_image(path: str, cache: bool, prune: bool, secrets: t.Dict[str, str] = None):
    dm = DockerManager(path)
    LOG.log("Building docker image...")
    abs_path = os.path.abspath(os.path.join(path, ".buildfile"))
    image = dm.build_image(
        dockerfile=abs_path, cache=cache, prune=prune, buildargs=secrets
    )

    return dm, image


def status_output(status, allowed_status_codes: t.List[int] = [0]):
    if status["StatusCode"] in allowed_status_codes:
        LOG.log("Success", color="green")
    else:
        LOG.log("Error", color="red")
        exit(1)


def validate_import(
    path: str, cache: bool, prune: bool, secrets: t.Dict[str, str] = None
):
    try:
        dm, image = build_image(path, cache=cache, prune=prune, secrets=secrets)
        LOG.log("=== VALIDATE IMPORT STEP ===")
        status, _ = dm.test_import(image)
        status_output(status)
        if prune:
            dm.remove_image(image=image)

    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def validate_endpoint_sample(
    path: str, cache: bool, prune: bool, secrets: t.Dict[str, str] = None
):
    try:
        LOG.log("=== VALIDATE ENDPOINT SAMPLE DATA STEP ===")
        dm, image = build_image(path, cache=cache, prune=prune, secrets=secrets)
        status, _ = dm.test_endpoint_sample(image)
        status_output(status)
        if prune:
            dm.remove_image(image=image)

    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def validate_unittest(
    path: str, cache: bool, prune: bool, secrets: t.Dict[str, str] = None
):
    try:
        dm, image = build_image(path=path, cache=cache, prune=prune, secrets=secrets)
        LOG.log("=== VALIDATE UNITTEST STEP ===")
        status, _ = dm.test_unittest(image)
        status_output(status, [0, 5])
        if prune:
            dm.remove_image(image=image)

    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def validate_integration(
    path: str,
    cache: bool,
    prune: bool,
    timeout: int,
    retries: int,
    secrets: t.Dict[str, str] = None,
):
    try:
        dm, image = build_image(path, cache=cache, prune=prune, secrets=secrets)
        LOG.log("=== VALIDATE INTEGRATION STEP ===")
        LOG.log("Waiting for service to start...")
        (
            rest_response,
            grpc_response,
            arrow_container,
            rest_container,
        ) = dm.run_and_check_health(
            image,
            kill_on_success=True,
            auth_enabled=False,
            timeout=timeout,
            retries=retries,
        )
        if _validate_container_response(
            rest_response=rest_response, grpc_response=grpc_response
        ):
            LOG.log("Success", color="green")
        else:
            LOG.log(
                "Unable to run container. See stack trace for more info", color="red"
            )
            exit(1)
        if prune:
            dm.remove_image(image=image)

    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def validate_profiling(
    path: str,
    cache: bool,
    prune: bool,
    timeout: int,
    retries: int,
    secrets: t.Dict[str, str] = None,
):
    try:
        dm, image = build_image(path, cache=cache, prune=prune, secrets=secrets)
        LOG.log("=== VALIDATE PROFILING STEP ===")
        LOG.log("Initiating service...")
        (
            rest_response,
            grpc_response,
            arrow_container,
            rest_container,
        ) = dm.run_and_check_health(
            image,
            kill_on_success=False,
            auth_enabled=False,
            timeout=timeout,
            retries=retries,
        )
        success = _validate_container_response(
            rest_response=rest_response, grpc_response=grpc_response
        )
        if not success:
            LOG.log(
                "Failed to run service container, ensure service can run with `tktl validate integration`",
                color="red",
            )
            exit(1)
        try:
            LOG.log("Initiating remote profiling...")
            status, container = dm.run_profiling_container()
            status_output(status)
            if prune:
                dm.remove_image(image=container.image.id)
        finally:
            try:
                arrow_container.kill()
                rest_container.kill()
                if prune:
                    dm.remove_image(image=rest_container.image.id)
                    dm.remove_image(image=arrow_container.image.id)
            except APIError:
                pass

    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def _validate_rest_response(rest_response):
    if rest_response is None:
        LOG.log("Could not access REST endpoint", color="red")
    elif rest_response.status_code != 204:
        LOG.log(f"Response status code {rest_response.status_code}", color="red")
    else:
        return True
    return False


def _validate_grpc_response(grpc_response):
    if grpc_response is None:
        LOG.log("Could not access gRPC endpoint", color="red")
    else:
        return True
    return False


def _validate_container_response(rest_response, grpc_response):
    return _validate_rest_response(
        rest_response=rest_response
    ) and _validate_grpc_response(grpc_response=grpc_response)


def validate_all(
    path: str,
    cache: bool,
    prune: bool,
    timeout: int,
    retries: int,
    secrets: t.Dict[str, str] = None,
):
    validate_project_config(path)
    validate_import(path, cache=cache, prune=prune, secrets=secrets)
    validate_endpoint_sample(path, cache=cache, prune=prune, secrets=secrets)
    validate_unittest(path, cache=cache, prune=prune, secrets=secrets)
    validate_integration(
        path,
        cache=True,
        prune=prune,
        timeout=timeout,
        retries=retries,
        secrets=secrets,
    )
    validate_profiling(
        path,
        cache=True,
        prune=prune,
        timeout=timeout,
        retries=retries,
        secrets=secrets,
    )
