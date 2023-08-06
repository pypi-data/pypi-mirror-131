from logging import debug
from cli_ui import debug as verbose

from gitlabform.gitlab import GitLab
from gitlabform.processors.abstract_processor import AbstractProcessor
from gitlabform.processors.util.difference_logger import DifferenceLogger


class ProjectSettingsProcessor(AbstractProcessor):
    def __init__(self, gitlab: GitLab):
        super().__init__("project_settings", gitlab)

    def _process_configuration(self, project_and_group: str, configuration: dict):
        project_settings = configuration["project_settings"]
        debug(
            "Project settings BEFORE: %s",
            self.gitlab.get_project_settings(project_and_group),
        )
        verbose(f"Setting project settings: {project_settings}")
        self.gitlab.put_project_settings(project_and_group, project_settings)
        debug(
            "Project settings AFTER: %s",
            self.gitlab.get_project_settings(project_and_group),
        )

    def _print_diff(self, project_and_group: str, project_settings):
        current_project_settings = self.gitlab.get_project_settings(project_and_group)
        DifferenceLogger.log_diff(
            "Project %s changes" % project_and_group,
            current_project_settings,
            project_settings,
        )
