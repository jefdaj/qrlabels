#!/usr/bin/env python

# TODO add features:
#      - flags for the margins
#      - flags for nrow, ncol
#      - flag for nchar
#      - print list of codes from file given on CLI
#      - verbose option that prints codes
#      - do multiple pages at once (via -n (npages) flag or passing codes)
#      - flag to print a bunch of sizes for testing?
#      - do groups of repeated barcodes (and generate proper innergrid)

# TODO remove settings once printed on paper:
#      - any qr size .30-.35 works great with spot-2000 on white boxes
#      - 0.18 is best for spot-1000 on the sides of 200uL tubes (trickiest location)
#      - 0.22 is good for spot-1000 otherwise
#      - 0.45 margins for all

'''
Generates PDFs of QR codes to print on labels.

Usage:
  qrlabels [-v] -p <prefix> <pdfpath>
  qrlabels --help

Options:
  --help        Show this text
  -v            Print debugging messages to stdout [defualt: False]
  -p <prefix>   Text to append the UUIDs to, for example "http://my.site/qrcode/"
     <pdfpath>  Where to write the QR code images
'''

from docopt                        import docopt
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes     import Drawing
from reportlab.lib.colors          import lightgrey
from reportlab.lib.pagesizes       import letter, inch
from reportlab.lib.styles          import getSampleStyleSheet
from reportlab.platypus            import SimpleDocTemplate, TableStyle, Paragraph
from reportlab.platypus.tables     import Table
from shortuuid                     import uuid
from sys                           import argv

def qrcode(prefix, nchar):
  return QrCodeWidget(prefix + uuid()[:nchar])

def qrcodes(prefix, nchar, nrow, ncol, qrsize):
  rows = []
  for r in range(1, nrow+1):
    row = []
    for c in range(1, ncol+1):
      qrc = qrcode(prefix, nchar)
      bounds = qrc.getBounds()
      label  = Drawing(qrsize, qrsize, transform=[qrsize/bounds[2], 0, 0,
                                                  qrsize/bounds[3], 0, 0])
      label.add(qrc)
      row.append(label)
    rows.append(row)
  return rows

def table(doc, style, prefix, nchar, nrow, ncol, qrsize):
  label_widths  = [doc.width  / ncol] * ncol
  label_heights = [(doc.height - style.leading) / nrow] * nrow
  data = qrcodes(prefix, nchar, nrow, ncol, qrsize)
  tbl = Table(data, colWidths=label_widths, rowHeights=label_heights,
              hAlign='CENTER', vAlign='MIDDLE')
  tbl.setStyle(TableStyle([ ('ALIGN'    , (0,0), (-1,-1), 'CENTER'),
                            ('VALIGN'   , (0,0), (-1,-1), 'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 1.0, lightgrey),
                            ('BOX'      , (0,0), (-1,-1), 1.0, lightgrey) ]))
  return tbl

def kludge(canvas, doc):
  frame = doc.pageTemplates[0].frames[0]
  frame.leftPadding=frame.rightPadding=frame.topPadding=frame.bottomPadding=0
  canvas.saveState()

def pdf(prefix, nchar, ncol, nrow, filename):
  style = getSampleStyleSheet()['Normal']
  wm = Paragraph(' '.join(['qrlabels']+argv[1:]), style)
  doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin  = 0.45*inch,
                          leftMargin   = 0.45*inch,
                          topMargin    = 0.45*inch-style.leading,
                          bottomMargin = 0.45*inch)
  qrsize = 0.18 * inch
  t = table(doc, style, prefix, nchar, nrow, ncol, qrsize)
  return doc.build([wm, t], onFirstPage=kludge, onLaterPages=kludge)

def main():
  args = docopt(__doc__, version='qrlabels 0.1')
  global verbose; verbose = args['-v']
  pdf(args['-p'], 7, 12, 16, args['<pdfpath>'])
