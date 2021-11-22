from __future__ import unicode_literals
import frappe
from frappe import throw, _
import io
from barcode import Code128
from barcode.writer import SVGWriter
from frappe.model.naming import make_autoname

# from bglstore.item_controller import reset_bgls_naming_series
# frappe.call('bglstore.item_controller.reset_bgls_naming_series', {
#     current: '5'
# }).then(r => {
#     console.log(r.message)
# })
@frappe.whitelist()
def reset_bgls_naming_series(current=0):
	naming_series=frappe.db.sql("""UPDATE `tabSeries` set current=%(current)s where name='BGLS' 
				""",{"current":current},as_dict=True)	
	frappe.db.commit()
	result=frappe.db.sql("""select current from `tabSeries` where name='BGLS'""",as_dict=True)	
	return result
		

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
				else:
					file_exists=frappe.db.get_list('File', filters={'file_url': ['=', self.item_barcode_image_cf]})
					if len(file_exists)==0:
						item_barcode_cf = self.barcodes[0].barcode
						if item_barcode_cf:
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

