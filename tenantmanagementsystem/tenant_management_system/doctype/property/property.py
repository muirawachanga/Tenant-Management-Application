# Copyright (c) 2022
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document


class Property(Document):

    def validate(self):
        if not self.property_cost_center:
            self.create_cost_center()

    @frappe.whitelist()
    def create_cost_center(self):
        """
        Create cost center with the name of the property under the selected parent cost center
        """
        if self.property_name in (None, ""):
            frappe.msgprint(_("Please set Property Name first."))
            self.parent_cost_center = ""
            return
        from erpnext.setup.doctype.company.company import get_name_with_abbr

        real_name = get_name_with_abbr(self.property_name, self.company)
        # Check if the cost center exists before creating
        if frappe.db.exists("Cost Center", real_name):
            cost_c = frappe.get_doc("Cost Center", real_name)
            if cost_c.parent_cost_center == self.parent_cost_center:
                self.property_cost_center = cost_c.name
                return
            frappe.msgprint(
                _(
                    "A Cost Center with this property name exists under another parent. You can make changes only in Cost Centers."
                )
            )
            self.parent_cost_center = cost_c.parent_cost_center
            return

        cost_c = frappe.get_doc(
            {
                "doctype": "Cost Center",
                "cost_center_name": self.property_name,
                "parent_cost_center": self.parent_cost_center,
                "company": self.company,
                "is_group": 0,
            }
        )
        frappe.db.begin()
        cost_c = cost_c.insert()
        frappe.db.commit()
        self.property_cost_center = cost_c.name
