// # Copyright (c) 2022
// # For license information, please see license.txt

cur_frm.add_fetch()
var lock_tc_items = 0;
var loaded_tc_items = [];

frappe.ui.form.on('Tenancy Contract', {
    onload: function(frm) {

    },
    refresh: function(frm) {
        if(frm.doc.__islocal){
            frm.set_query('property_unit', function(){
                return {
                    query: "tenantmanagementsystem.tenant_management_system.doctype.property_unit.property_unit.property_unit_query",
                    filters: {
                        tc_filters: ['Active', 'New'],
                        side: 'not in'
                    }
                }
            });
        }
        if (frm.doc.contract_status == 'Active' || frm.doc.contract_status == 'Suspended') {
            frm.add_custom_button(__("Create Invoice"), function() {
                frm.events.make_invoice(frm);
            }).addClass("btn-primary");
        }

        if (frm.doc.contract_status !== "New") {
            frm.toggle_enable('*', 0);
            if (frm.doc.contract_status != 'Terminated') {
                frm.toggle_enable(['items','grace_period', 'auto_generate_invoice', 'email_invoice', 'termination_date'], 1);
            }
            frappe.call({
                method: "tenantmanagementsystem.tenant_management_system.doctype.property_management_settings.property_management_settings.load_configuration",
                args: {
                    "name": 'lock_tenancy_contract_items',
                    "default": 1
                },
                callback: function(r) {
                    if (!r.exc){
                        if(r.message) {
                            lock_tc_items = r.message;
                        }else{
                            lock_tc_items = 0;
                        }
                        if(lock_tc_items) {
                            frm.toggle_enable('items', 0);
                            frm.events.disable_items(frm);
                            var items_grid = frm.fields_dict["items"].grid;
                            loaded_tc_items = items_grid.get_data();
                        }else{
                            frm.toggle_enable('items', 1);
                        }
                    } else {
                        msgprint(__("Failed to load required configuration! Please contact support."), __("Warning!"));
                    }

                }
            });
        }
    },
    validate: function(frm) {
        if (!frm.doc.start_date && frm.doc.contract_status == "Active") {
            msgprint(__("You must set the contract start date before approving"));
            validated = false;
            return
        }
        if (!frm.doc.end_date && frm.doc.contract_status == "Active") {
            msgprint(__("You must set the contract end date before approving"));
            validated = false;
            return
        }
        if (!frm.doc.termination_date && frm.doc.contract_status == "Terminated") {
            msgprint(__("Please set the contract termination date."));
            validated = false;
            return;
        }
        if (!frm.doc.cancellation_date && frm.doc.contract_status == "Cancelled") {
            frm.set_value('cancellation_date', get_today());
            validated = true;
        }

        if (frm.doc.contract_status != "New") {
            var items = frm.doc.items;
            if(!items.length){
                msgprint(__("You Cannot approve a tenancy contract with no billing items. Not Saved."));
                validated = false;
                return;
            }
            if (lock_tc_items) {
                var items_grid = frm.fields_dict["items"].grid;
                for (var i = 0; i < items.length; i++) {
                    if(items[i].is_utility_item){
                        if(!items[i].utility_item){
                            msgprint(__("Item: " + item[i].item_name + " is marked as Utility Item " +
                                "but has no Utility Item choosen"));
                            validated = false;
                            return;
                        }
                    }
                }
            }
            validated = true;
        }

    },

    make_invoice: function(frm) {
        frappe.model.open_mapped_doc({
            method: "tenantmanagementsystem.tenant_management_system.doctype.tenancy_contract.tenancy_contract.make_sales_invoice",
            frm: frm
        });
    },
    start_date: function(frm) {
        if (frm.doc.start_date) {
            frm.set_value('date_of_first_billing', frm.doc.start_date);
            var msg = __('Date of First Billing set to: ') + frm.doc.start_date + __('. Note that you can select a different date if you wish.');
            msgprint(msg);
        } else {

        }
    },
    end_date: function(frm) {
        if (frm.doc.start_date) {
            if (frappe.datetime.get_diff(frm.doc.start_date, frm.doc.end_date) > 0) {
                msgprint(__('End date cannot be earlier than start date.'));
                frm.set_value('end_date', '');
            }
            if (frappe.datetime.get_diff(frm.doc.date_of_first_billing, frm.doc.end_date) > 0) {
                msgprint(__('End date cannot be earlier than Date of First Billing.'));
                frm.set_value('end_date', '');
            }
        }
    },
    date_of_first_billing: function(frm) {
        if (frm.doc.start_date) {
            if (frappe.datetime.get_diff(frm.doc.start_date, frm.doc.date_of_first_billing) > 0) {
                msgprint(__('Date of First Billing cannot be earlier than start date.'));
                frm.set_value('date_of_first_billing', '');
            }
        }
    },
    property_unit: function(frm) {
        if (!frm.doc.property_unit) {
            frm.set_value("property_name", "");
            frm.set_value("property_unit_name", "");
        } else {
            frappe.model.get_value("Property Unit", frm.doc.property_unit, "property", function(value) {
                frappe.model.with_doc("Property", value.property, function(r) {
                    var p = frappe.model.get_doc("Property", value.property);
                    frm.set_value("property_name", p.property_name);
                });
            });
        }
    },
    disable_items: function(frm){
        var item_grid = frm.fields_dict["items"].grid;
        var ignore_field_types = ['Column Break', 'Section Break'];
        var ignore_fields = ['description', 'stock_uom', 'income_account', 'cost_center'];
        $.each(item_grid.docfields, function(i, val){
            if($.inArray(val.fieldtype, ignore_field_types) !== -1) return;
            if($.inArray(val.fieldname, ignore_fields)  !== -1) return;
            item_grid.toggle_enable(val.fieldname, 0);
        })
    }
});


cur_frm.cscript.item_code = function(doc, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.item_code) {
        return frappe.call({
            method: "tenantmanagementsystem.tenant_management_system.doctype.tenancy_contract.tenancy_contract.get_item_details",
            args: {
                "item_code": d.item_code,
                "start_date": cur_frm.doc.start_date
            },
            callback: function(r, rt) {
                if (r.message) {
                    $.each(r.message, function(k, v) {
                        frappe.model.set_value(cdt, cdn, k, v);
                    });
                    refresh_field('image_view', d.name, 'items');
                }
            }
        })
    }
};

cur_frm.cscript.remit_full_amount = function(doc, cdt, cdn) {
    if (frappe.model.get_value(cdt, cdn, "remit_full_amount")) {
        frappe.model.set_value(cdt, cdn, "remmitable", 1);
        var f = frappe.utils.filter_dict(cur_frm.fields_dict["items"].grid.grid_rows_by_docname[cdn].docfields, {
            'fieldname': "remmitable"
        })[0];
        f.read_only = 1;
        cur_frm.fields_dict["items"].grid.grid_rows_by_docname[cdn].fields_dict["remmitable"].refresh();
    } else {
        var f = frappe.utils.filter_dict(cur_frm.fields_dict["items"].grid.grid_rows_by_docname[cdn].docfields, {
            'fieldname': "remmitable"
        })[0];
        f.read_only = 0;
        cur_frm.fields_dict["items"].grid.grid_rows_by_docname[cdn].fields_dict["remmitable"].refresh();
    }
};



