# Copyright (c) 2022, Bituls Company Limited and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = []
    prop = filters.get("property")
    billing_period = filters.get("billing_period")
    prop_type = filters.get("property_type")
    # Prepare the filter to get all property
    property_filter = {"company": filters.get("company")}
    paid_sales_filters = {
        "Status": ["in", ["Paid"]],
    }
    unpaid_sales_filters = {
        "Status": ["in", ["Unpaid", "Overdue"]],
    }
    if prop and prop_type or billing_period:
        property_filter = {
            "company": filters.get("company"),
            "type": prop_type,
            "name": prop,
        }
        paid_sales_filters = {
            "Status": ["in", ["Paid"]],
            "billing_period": billing_period,
        }
        unpaid_sales_filters = {
            "Status": ["in", ["Unpaid", "Overdue"]],
            "billing_period": billing_period,
        }
    elif prop:
        property_filter = {"company": filters.get("company"), "name": prop}
    elif prop_type:
        property_filter = {
            "company": filters.get("company"),
            "type": prop_type,
        }
    elif billing_period:
        paid_sales_filters = {
            "Status": ["in", ["Paid"]],
            "billing_period": billing_period,
        }
        unpaid_sales_filters = {
            "Status": ["in", ["Unpaid", "Overdue"]],
            "billing_period": billing_period,
        }
    data = frappe.db.get_all(
        "Property",
        filters=property_filter,
        fields=["name", "type", "property_name"],
        order_by="creation",
    )
    for property in data:
        paid_sales_filters.update({"property_name": property.property_name})
        unpaid_sales_filters.update({"property_name": property.property_name})
        property["paid_sales_invoice"] = frappe.db.count(
            "Sales Invoice", filters=paid_sales_filters
        )
        property["unpaid_sales_invoice"] = frappe.db.count(
            "Sales Invoice", filters=unpaid_sales_filters
        )
        property["total_occupied"] = frappe.db.count(
            "Tenancy Contract",
            filters={
                "contract_status": "Active",
                "property_name": property.property_name,
            },
        )
        property["total_unoccupied"] = (
            frappe.db.count("Property Unit", filters={"property": property.name})
            - property["total_occupied"]
        )
    chart = get_chart_data(data)
    report_summary = get_report_summary(data)
    return columns, data, None, chart, report_summary


def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("Property"),
            "fieldtype": "Link",
            "options": "Property",
            "width": 200,
        },
        {
            "fieldname": "property_name",
            "label": _("Property Name"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "type",
            "label": _("Type"),
            "fieldtype": "Link",
            "options": "Project Type",
            "width": 120,
        },
        {
            "fieldname": "paid_sales_invoice",
            "label": _("Total Paid Units"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "unpaid_sales_invoice",
            "label": _("Total UnPaid Units"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "total_occupied",
            "label": _("Total Occupied Units"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "total_unoccupied",
            "label": _("Total Unoccupied Units"),
            "fieldtype": "Data",
            "width": 200,
        },
    ]


def get_chart_data(data):
    labels = []
    paid_sales_invoice = []
    unpaid_sales_invoice = []
    total_occupied = []
    total_unoccupied = []

    for property in data:
        labels.append(property.name + "-" + property.property_name)
        paid_sales_invoice.append(property.paid_sales_invoice)
        unpaid_sales_invoice.append(property.unpaid_sales_invoice)
        total_occupied.append(property.total_occupied)
        total_unoccupied.append(property.total_unoccupied)

    return {
        "data": {
            "labels": labels[:30],
            "datasets": [
                {"name": "Paid Units", "values": paid_sales_invoice[:30]},
                {"name": "Unpaid Units", "values": unpaid_sales_invoice[:30]},
                {"name": "Occupied Units", "values": total_occupied[:30]},
                {"name": "Unoccupied Units", "values": total_unoccupied[:30]},
            ],
        },
        "type": "bar",
        "colors": ["#7575ff", "#fc4f51", "#78d6ff", "#eba00c"],
        "barOptions": {"stacked": True},
    }


def get_report_summary(data):
    if not data:
        return None
    paid_sales_invoice = sum([property.paid_sales_invoice for property in data])
    unpaid_sales_invoice = sum([property.unpaid_sales_invoice for property in data])
    total_occupied = sum([property.total_occupied for property in data])
    total_unoccupied = sum([property.total_unoccupied for property in data])
    return [
        {
            "value": paid_sales_invoice,
            "indicator": "Green"
            if unpaid_sales_invoice >= paid_sales_invoice
            else "Red",
            "label": _("Paid Units"),
            "datatype": "Int",
        },
        {
            "value": unpaid_sales_invoice,
            "indicator": "Blue" if unpaid_sales_invoice == 0 else "Red",
            "label": _("Unpaid Units"),
            "datatype": "Int",
        },
        {
            "value": total_occupied,
            "indicator": "Green" if total_occupied <= total_unoccupied else "Red",
            "label": _("Occupied Units"),
            "datatype": "Int",
        },
        {
            "value": total_unoccupied,
            "indicator": "Yellow" if total_unoccupied == 0 else "Red",
            "label": _("Unoccupied Units"),
            "datatype": "Int",
        },
    ]
