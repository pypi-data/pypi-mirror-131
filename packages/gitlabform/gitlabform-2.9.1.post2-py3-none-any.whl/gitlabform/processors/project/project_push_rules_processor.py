from logging import debug
from cli_ui import debug as verbose

from gitlabform.gitlab import GitLab
from gitlabform.processors.abstract_processor import AbstractProcessor
from gitlabform.processors.util.difference_logger import DifferenceLogger


class ProjectPushRulesProcessor(AbstractProcessor):
    def __init__(self, gitlab: GitLab):
        super().__init__("project_push_rules", gitlab)

    def _process_configuration(self, project_and_group: str, configuration: dict):
        push_rules = configuration["project_push_rules"]
        old_project_push_rules = self.gitlab.get_project_push_rules(project_and_group)
        debug("Project push rules settings BEFORE: %s", old_project_push_rules)
        if old_project_push_rules:
            verbose(f"Updating project push rules: {push_rules}")
            self.gitlab.put_project_push_rules(project_and_group, push_rules)
        else:
            verbose(f"Creating project push rules: {push_rules}")
            self.gitlab.post_project_push_rules(project_and_group, push_rules)
        debug(
            "Project push rules AFTER: %s",
            self.gitlab.get_project_push_rules(project_and_group),
        )

    def _print_diff(self, project_and_group: str, push_rules):
        current_push_rules = self.gitlab.get_project_push_rules(project_and_group)
        DifferenceLogger.log_diff(
            "Project %s push rules changes" % project_and_group,
            current_push_rules,
            push_rules,
        )
