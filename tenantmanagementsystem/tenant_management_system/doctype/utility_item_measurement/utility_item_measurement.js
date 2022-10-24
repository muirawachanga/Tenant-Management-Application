// # Copyright (c) 2022
// # For license information, please see license.txt

frappe.ui.form.on('Utility Item Measurement', {
    onload: function (frm) {
        frm.add_fetch('property_unit', 'unit_name', 'property_unit_name');
        frm.add_fetch('tenancy_contract', 'customer', 'customer_name');
        frm.add_fetch('property', 'property_name', 'property_name');
    },
    refresh: function (frm) {
        frm.toggle_display(['meter_reading', 'usage_units', 'monetary_amount'], 0);
        frm.toggle_reqd(['meter_reading', 'usage_units', 'monetary_amount'], 0);
        if(frm.doc.utility_item){
            frm.events.enable_measure(frm);
        }
        if(frm.doc.__islocal){
            frm.set_query('property_unit', function(){
                return {
                    query: "tenantmanagementsystem.tenant_management_system.doctype.property_unit.property_unit.property_unit_query",
                    filters: {
                        tc_filters: ['Active'],
                        side: 'in',
                        property: frm.doc.property
                    }
                }
            });
        }
    },
    property_unit: function (frm) {
        frappe.model.get_value('Tenancy Contract', {
            "property_unit": frm.doc.property_unit,
            "contract_status": 'Active'
        }, 'name', function (value) {
            frm.set_value('tenancy_contract', value.name || '');
        });
    },
    tenancy_contract: function (frm) {
        frappe.model.get_value('Tenancy Contract', {
            "property_unit": frm.doc.property_unit,
            "contract_status": 'Active'
        }, 'customer', function (value) {
            frm.set_value('customer_name', value.customer);
        });
        if(frm.doc.tenancy_contract){
            frm.set_query('utility_item', function(doc, doctype, doc_name){
                return {
                    query: "tenantmanagementsystem.tenant_management_system.doctype.utility_item.utility_item.utility_item_query",
                    filters: {
                        "tenancy_contract": doc.tenancy_contract
                    }
                }
            });
        }else{
            frm.set_query('utility_item', function(doc, doctype, doc_name){
                return {
                    filters: {

                    }
                }
            });
        }
    },
    utility_item: function(frm){
        if(frm.doc.utility_item) {
            frm.events.enable_measure(frm);
        }
    },
    enable_measure: function(frm){
        frappe.model.with_doc('Utility Item', frm.doc.utility_item, function(){
            var ui_doc = frappe.model.get_doc('Utility Item', frm.doc.utility_item);
            if(ui_doc.measurement_type === 'Meter Reading'){
                frm.toggle_display('meter_reading', 1);
                frm.toggle_reqd('meter_reading', 1);
            }
            if(ui_doc.measurement_type === 'Usage Units'){
                frm.toggle_display('usage_units', 1);
                frm.toggle_reqd('usage_units', 1);
            }
            if(ui_doc.measurement_type === 'Monetary Amount'){
                frm.toggle_display('monetary_amount', 1);
                frm.toggle_reqd('monetary_amount', 1);
            }
            if(frm.doc.measurement_status === 'Billed'){
                frm.toggle_enable('*', 0);
                if(ui_doc.measurement_type === 'Meter Reading') {
                    frm.toggle_display('usage_units', 1);
                }
            }
        });
    }
});

