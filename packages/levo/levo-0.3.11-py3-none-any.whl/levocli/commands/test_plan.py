"""Test Plan related sub commands"""

import logging
import tempfile
from typing import Dict, Optional, Tuple

import click
from click_loglevel import LogLevel
from schemathesis.cli import callbacks as schemathesis_cli_callbacks

from levocli.commands.constants import *

from .. import callbacks, runners
from ..config import TestPlanCommandConfig
from ..logger import set_log_level
from ..login import login_or_refresh

TARGET_URL_OPTION = "--target-url"
TARGET_URL_OPTION_HELP = (
    "--target-url must specify a valid URL pointing to a live host that implements the endpoints"
    " that are present in the test plan."
)

TEST_PLAN_OPTION = "--test-plan"
TEST_PLAN_OPTION_HELP = (
    "--test-plan must specify a valid Levo Resource Name (LRN)"
    " or an absolute path to a Levo Test Plan folder."
)

ENV_FILE_OPTION = "--env-file"
ENV_FILE_OPTION_HELP = (
    "Path to YAML file with environment definitions (AuthN/AuthZ info, etc.)."
)

"""Helper functions"""


def _execute_test_plan(
    test_plan: str,
    target_url: str,
    auth: Optional[Tuple[str, str]],
    auth_type: str,
    disable_reporting_to_saas: bool,
    headers: Dict[str, str],
    verbosity: LogLevel,
    env_file: Optional[str],
    show_errors_tracebacks: bool = False,
):
    """Execute a test plan"""
    set_log_level(int(verbosity))
    config = TestPlanCommandConfig(
        target_url=target_url,
        testplan_ref=test_plan,
        auth=auth,
        auth_type=auth_type,
        report_to_saas=not disable_reporting_to_saas,
        headers=headers,
        env_file_path=env_file,
        show_errors_tracebacks=show_errors_tracebacks,
    )
    runners.levo_plans.validate_argument_constraints(config)
    login_or_refresh()
    runners.levo_plans.cli_entrypoint(config)


""" End of Helper Functions Section"""


"""test-plan sub commands"""


@click.group(context_settings=CONTEXT_SETTINGS)
def test_plan():
    """Test plan management sub commands."""
    return


@test_plan.command(short_help="Run a test plan against the specified target-url.")
@click.option(
    TARGET_URL_OPTION,
    help=TARGET_URL_OPTION_HELP,
    type=str,
    required=True,
    callback=callbacks.validate_target_url,
)
@click.option(
    AUTH_OPTION,
    AUTH_OPTION_SHORT,
    help=AUTH_OPTION_HELP,
    type=str,
    callback=schemathesis_cli_callbacks.validate_auth,
)
@click.option(
    AUTH_TYPE_OPTION,
    AUTH_TYPE_OPTION_SHORT,
    type=click.Choice(AUTH_TYPE_OPTION_CHOICES, case_sensitive=False),
    default=AUTH_TYPE_OPTION_CHOICES_DEFAULT,
    help=AUTH_TYPE_OPTION_HELP,
    show_default=True,
)
@click.option(
    NO_REPORTS_TO_SAAS_OPTION,
    is_flag=True,
    help=NO_REPORTS_TO_SAAS_HELP,
)
@click.option(
    TEST_PLAN_OPTION,
    help=TEST_PLAN_OPTION_HELP,
    type=str,
    required=True,
)
@click.option(
    HEADER_OPTION,
    HEADER_OPTION_SHORT,
    "headers",
    help=HEADER_OPTION_HELP,
    multiple=True,
    type=str,
    callback=callbacks.validate_headers,
)
@click.option(
    ERROR_TRACE_OPTION,
    help=ERROR_TRACE_OPTION_HELP,
    is_flag=True,
    is_eager=True,
    default=False,
    show_default=True,
)
@click.option(
    ENV_FILE_OPTION,
    help=ENV_FILE_OPTION_HELP,
    type=str,
    default=None,
)
@click.option(
    VERBOSITY_OPTION_SHORT,
    VERBOSITY_OPTION,
    type=LogLevel(),
    default=logging.WARN,
)
def run(
    test_plan: str,
    target_url: str,
    auth: Optional[Tuple[str, str]],
    auth_type: str,
    disable_reporting_to_saas: bool,
    headers: Dict[str, str],
    verbosity: LogLevel,
    env_file: Optional[str],
    show_errors_tracebacks: bool = False,
):
    """Run a test plan against the specified target-url."""
    _execute_test_plan(
        test_plan,
        target_url,
        auth,
        auth_type,
        disable_reporting_to_saas,
        headers,
        verbosity,
        env_file,
        show_errors_tracebacks,
    )


@test_plan.command(
    short_help="Export a test plan from Levo SaaS to the local file system.",
    context_settings={
        **CONTEXT_SETTINGS,  # type: ignore
    },
)
@click.option(
    "--lrn",
    type=str,
    required=True,
    help="The LRN of the test plan you want to export.",
)
@click.option(
    "--local-dir",
    type=str,
    default=None,
    help="Path to a local directory where the test plan is to be exported.",
)
@click.option(
    "-v",
    "--verbosity",
    type=LogLevel(),
    default=logging.WARN,
    help=DEBUG_SETTINGS_HELP,
)
def export(
    plan_lrn: str,
    local_dir: Optional[str],
    verbosity: LogLevel,
) -> None:
    set_log_level(int(verbosity))
    login_or_refresh()

    path = local_dir if local_dir else tempfile.mkdtemp()
    runners.levo_plans.export_plan(plan_lrn, path)


"""Test command is an alias command for 'test-plan run'"""


@click.command(
    short_help="Execute a test plan against the specified target-url.",
    context_settings={
        **CONTEXT_SETTINGS,  # type: ignore
    },
)
@click.option(
    TARGET_URL_OPTION,
    help=TARGET_URL_OPTION_HELP,
    type=str,
    required=True,
    callback=callbacks.validate_target_url,
)
@click.option(
    AUTH_OPTION,
    AUTH_OPTION_SHORT,
    help=AUTH_OPTION_HELP,
    type=str,
    callback=schemathesis_cli_callbacks.validate_auth,
)
@click.option(
    AUTH_TYPE_OPTION,
    AUTH_TYPE_OPTION_SHORT,
    type=click.Choice(AUTH_TYPE_OPTION_CHOICES, case_sensitive=False),
    default=AUTH_TYPE_OPTION_CHOICES_DEFAULT,
    help=AUTH_TYPE_OPTION_HELP,
    show_default=True,
)
@click.option(
    NO_REPORTS_TO_SAAS_OPTION,
    is_flag=True,
    help=NO_REPORTS_TO_SAAS_HELP,
)
@click.option(
    TEST_PLAN_OPTION,
    help=TEST_PLAN_OPTION_HELP,
    type=str,
    required=True,
)
@click.option(
    HEADER_OPTION,
    HEADER_OPTION_SHORT,
    "headers",
    help=HEADER_OPTION_HELP,
    multiple=True,
    type=str,
    callback=callbacks.validate_headers,
)
@click.option(
    ERROR_TRACE_OPTION,
    help=ERROR_TRACE_OPTION_HELP,
    is_flag=True,
    is_eager=True,
    default=False,
    show_default=True,
)
@click.option(
    ENV_FILE_OPTION,
    help=ENV_FILE_OPTION_HELP,
    type=str,
    default=None,
)
@click.option(
    VERBOSITY_OPTION_SHORT,
    VERBOSITY_OPTION,
    type=LogLevel(),
    default=logging.WARN,
)
def test(
    test_plan: str,
    target_url: str,
    auth: Optional[Tuple[str, str]],
    auth_type: str,
    disable_reporting_to_saas: bool,
    headers: Dict[str, str],
    verbosity: LogLevel,
    env_file: Optional[str],
    show_errors_tracebacks: bool = False,
):
    """Execute a test plan against the specified target-url."""
    _execute_test_plan(
        test_plan,
        target_url,
        auth,
        auth_type,
        disable_reporting_to_saas,
        headers,
        verbosity,
        env_file,
        show_errors_tracebacks,
    )
