from __future__ import unicode_literals
import frappe
from frappe import throw, _
import io
from barcode import Code128
from barcode.writer import SVGWriter
from frappe.model.naming import make_autoname

def validate_and_create_barcode(self,method):
		if self.has_variants==0:
				if not self.item_barcode_image_cf:
					item_barcode_cf = make_autoname('BGLS.#',self.doctype)
					self.append('barcodes',{'barcode':item_barcode_cf,'barcode_type':''})

					buffer = io.BytesIO()
					Code128(str(item_barcode_cf), writer=SVGWriter()).write(buffer)
					_file = frappe.get_doc({
						"doctype": "File",
						"file_name": "%s.svg" % frappe.generate_hash()[:8],
						"attached_to_doctype": self.doctype,
						"attached_to_name": self.name,
						"attached_to_field":'item_barcode_image_cf',
						"content": buffer.getvalue()
					})
					_file.save()
					self.item_barcode_image_cf= _file.file_url