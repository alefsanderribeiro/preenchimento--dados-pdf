"""

Reading PDF Annotations
PDF 2.0 defines the following annotation types:

Text

Link

FreeText

Line

Square

Circle

Polygon

PolyLine

Highlight

Underline

Squiggly

StrikeOut

Caret

Stamp

Ink

Popup

FileAttachment

Sound

Movie

Screen

Widget

PrinterMark

TrapNet

Watermark

3D

Redact

Projection

RichMedia

In general, annotations can be read like this:
"""
from pypdf import PdfReader

reader = PdfReader("modelo.pdf")

for page in reader.pages:
    if "/Annots" in page:
        for annot in page["/Annots"]:
            obj = annot.get_object()
            
            print(obj)


