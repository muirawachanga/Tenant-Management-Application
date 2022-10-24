# Copyright (c) 2022
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.desk.reportview import get_match_cond
from frappe.model.document import Document


class PropertyUnit(Document):
    pass

    def validate(self):
        if self.property_name not in self.unit_name:
            combo_name = self.property_name + " - " + self.unit_name
            self.set("unit_name", combo_name)


@frappe.whitelist()
def property_unit_query(doctype, txt, searchfield, start, page_len, filters):
    # Select only property units that don't have Tenancy Contracts that are in specific statuses.
    # Specify these filters in filters["tc_filters"]. e.g:
    # Specify the 'side' (IN or NOT IN) using filters["side"]
    """
        frm.set_query('property_unit', function(){
                return {
                    query: "tenantmanagementsystem.tenant_management_system.doctype.property_unit.property_unit.property_unit_query",
                    filters: {
                        tc_filters: ['Active', 'New'],
                        side: "not in",
                        property: "PRO-00001"
                    }
                }
            })
    """
    property_filter = ""
    if filters.get("property"):
        property_filter = "and property = %s"
    prop = [] if not filters.get("property") else [filters.get("property")]

    return frappe.db.sql(
        "select name, unit_name from `tabProperty Unit` where name {side} "
        "(select property_unit from `tabTenancy Contract` where contract_status in "
        "({statuses})) and ({key} like %s or unit_name like %s) {prop} {mcond} "
        "order by if(locate(%s, name), locate(%s, name), 99999), "
        "if(locate(%s, unit_name), locate(%s, unit_name), 99999), "
        "idx desc, name, unit_name limit %s, %s".format(
            **{
                "key": searchfield,
                "mcond": get_match_cond(doctype),
                "side": filters["side"],
                "prop": property_filter,
                "statuses": ",".join(["%s"] * len(filters["tc_filters"])),
            }
        ),
        filters["tc_filters"]
        + ["%%%s%%" % txt, "%%%s%%" % txt]
        + prop
        + [
            txt.replace("%", ""),
            txt.replace("%", ""),
            txt.replace("%", ""),
            txt.replace("%", ""),
            start,
            page_len,
        ],
    )
