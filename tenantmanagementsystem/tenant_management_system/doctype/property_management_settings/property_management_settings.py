# Copyright (c) 2022
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class PropertyManagementSettings(Document):
    pass


@frappe.whitelist()
def load_configuration(name, default=None):
    val = frappe.db.get_single_value("Property Management Settings", name)
    if val is None:
        val = default
    return val
