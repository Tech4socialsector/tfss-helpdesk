__version__ = "1.22.2"
# Monkey patch Frappe's notify_assignment with branded version
import frappe.desk.form.assign_to as _assign_to
from helpdesk.overrides.assignment import notify_assignment as _branded_notify

_assign_to.notify_assignment = _branded_notify
# Monkey patch Frappe's notify_assignment with branded version
import frappe.desk.form.assign_to as _assign_to
from helpdesk.overrides.assignment import notify_assignment as _branded_notify
_assign_to.notify_assignment = _branded_notify

