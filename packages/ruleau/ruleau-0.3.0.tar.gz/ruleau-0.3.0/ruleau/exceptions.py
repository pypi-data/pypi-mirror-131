class RuleRequiresNameException(Exception):
    """Exception raised if a rule doesn't have a human readable name"""


class RuleRequiresIdException(Exception):
    """Exception raised if rule doesn't have an id"""


class MethodNotAllowedException(Exception):
    """Exception raised if a forbidden RuleauDict method is called"""


class CaseIdRequiredException(Exception):
    """Exception raised if a json path for case identifier is not found"""


class CannotOverrideException(Exception):
    """Exception raised if a API tries to override a rule marked as NO_OVERRIDE"""


class DuplicateRuleNameException(Exception):
    """Exception raised if more than 1 rule has same name"""

    def __init__(self, rule, conflict):
        self.rule = rule
        self.rule_name = rule.name
        self.rule_id = rule.id
        self.conflict_rule_name = conflict.name
        self.conflict_rule_id = conflict.id

        self.message = (
            f"The rule with id: {self.rule_id} - name: {self.rule_name} has a "
            f"name conflict.\nThe rule with id: {self.conflict_rule_id} - name: "
            f"{self.conflict_rule_name} is duplicated.\n"
        )


class RuleIdIllegalCharacterException(Exception):
    """Exception raise if Rule name contains illegal characters"""


class RuleFunctionNameAttributeCollisionException(Exception):
    """If the provided rule name collides with a rule attribute"""


class DuplicateRuleIdException(Exception):
    """Exception raised if more than 1 rule has same name"""

    def __init__(self, rule, conflict):
        self.rule = rule
        self.rule_name = rule.name
        self.rule_id = rule.id
        self.conflict_rule_name = conflict.name
        self.conflict_rule_id = conflict.id

        self.message = (
            f"The rule with id: {self.rule_id} - name: {self.rule_name} has an "
            f"ID conflict\nThe rule with id: {self.conflict_rule_id} - name: "
            f"{self.conflict_rule_name} is duplicated.\n"
        )


class APIException(Exception):
    """Generic exception for API request failure"""


class ConditionalDependencyReusedException(Exception):
    """Exception raised if the rule has duplicate dependencies"""


class RuleErrorException(Exception):
    """Exception raised when a rule raises an exception"""

    def __init__(self, rule, rule_exception):
        self.rule = rule
        self.rule_exception = rule_exception


class RunIfRuleHasRunIfException(Exception):
    """Exception raise if a run_if dependency of a rule also has a run_if."""


class RunIfAndRunIfNotSameRule(Exception):
    """The required keynames context and payload have not been provided"""

    def __init__(self, rule):
        self.rule_name = rule.name
        self.rule_id = rule.id
        self.message = (
            f"The rule with id: {self.rule_id} - name: {self.rule_name} has an issue.\n"
            f"The run_if and run_if_not are linked to the same rule {rule.run_if.id} "
            f"which will cause an invalid state."
        )
        super().__init__(self.message)


class IncorrectKwargsForDoctests(Exception):
    """The required keynames context and payload have not been provided"""

    def __init__(self, rule):
        self.rule_name = rule.name
        self.rule_id = rule.id
        self.message = (
            f"The rule with id: {self.rule_id} - name: {self.rule_name} has not "
            f"been defined with the correct keyword argument names.\n Please "
            f"change the rule argument names to context and payload."
        )
        super().__init__(self.message)
