# Copyright (c) 2022
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date
from frappe.utils import get_first_day, get_last_day, formatdate


class BillingPeriod(Document):
    pass
