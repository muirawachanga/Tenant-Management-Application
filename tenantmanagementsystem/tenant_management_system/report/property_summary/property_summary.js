// Copyright (c) 2022, Bituls Company Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Property Summary"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "property",
			"label": __("Property"),
			"fieldtype": "Link",
			"options": "Property"
		},	
		{
			"fieldname": "tenancy_status",
			"label": __("Tenancy Status"),
			"fieldtype": "Select",
			"options": "\nNew\nActive\nSuspended\nCancelled\nTerminated\nRejected",
			"default": "Active",
		},
		{
			"fieldname": "billing_period",
			"label": __("Billing Period"),
			"fieldtype": "Link",
			"options": "Billing Period"
		},
		{
			"fieldname": "property_type",
			"label": __("Property Type"),
			"fieldtype": "Link",
			"options": "Property Type"
		}
	]
};

