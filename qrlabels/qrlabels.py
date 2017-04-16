#!/usr/bin/env python

# TODO refactor CLI:
#      - remove idlist for now
#      - remove history for now
#      - replace outdir with a pdf path
#      - add a flag for each measurement i've been changing

# TODO quick documentation:
#      - print settings (100% scale, highest quality)
#      - examples (do after CLI)

# TODO refactor code:
#      - break up into smaller, more meaningful functions
#      - make variable names sensible

# TODO add features:
#      - print list of codes from file given on CLI
#      - verbose option that prints codes
#      - do multiple pages at once (via flag or passing codes)
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
  qrlabels [-v] [-p <prefix>] (-i <idlist> | -n <number>) [-h <history>] [-o <outdir>]

Options:
  -v            Print debugging messages to stdout [defualt: False]
  -p <prefix>   Text to append the UUIDs to, for example "knlab/jj/". [default: ]
  -i <idlist>   List of UUIDs to generate QR codes for
  -n <number>   Number of UUIDs to generate
  -h <history>  Append UUIDs to a history file to prevent accidental repeats
  -o <outdir>   Where to write the QR code images [default: .]
'''

from reportlab.lib.colors       import lightgrey
from docopt                     import docopt
from math                       import sqrt
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes  import Drawing 
from reportlab.lib.pagesizes    import letter, inch
from reportlab.lib.styles       import getSampleStyleSheet
from reportlab.platypus         import SimpleDocTemplate, TableStyle, Paragraph
from reportlab.platypus.tables  import Table
from shortuuid                  import uuid
from sys import argv

def generate_qrcode(prefix, nchar):
  return qr.QrCodeWidget(prefix + uuid()[:nchar])

def fix_page_layout(canv, doc):
  frame = doc.pageTemplates[0].frames[0]
  frame.leftPadding=frame.rightPadding=frame.topPadding=frame.bottomPadding=0
  canv.saveState()

def save_pdf(prefix, nchar, ncol, nrow, filename):
  s = getSampleStyleSheet()['Normal']
  wm = Paragraph(' '.join(['qrlabels']+argv[1:]), s)
  doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=0.45*inch, leftMargin=0.45*inch,
                          topMargin=0.45*inch-s.leading, bottomMargin=0.45*inch)
  qw = doc.width  / ncol
  qh = (doc.height - s.leading) / nrow
  rws = [qw] * ncol
  rhs = [qh] * nrow
  ls = 0.18 * inch
  rows = []
  for r in range(1, nrow+1):
    row = []
    for c in range(1, ncol+1):
      qrcode = generate_qrcode(prefix, nchar)
      bounds = qrcode.getBounds()
      width  = bounds[2]
      height = bounds[3]
      label  = Drawing(ls, ls, transform=[ls/width, 0, 0, ls/height, 0, 0])
      label.add(qrcode)
      row.append(label)
    rows.append(row)
  t = Table(rows, colWidths=rws, rowHeights=rhs, hAlign='CENTER', vAlign='MIDDLE')
  t.setStyle(TableStyle([ ('ALIGN'    , (0,0), (-1,-1), 'CENTER'),
                          ('VALIGN'   , (0,0), (-1,-1), 'MIDDLE'),
                          ('INNERGRID', (0,0), (-1,-1), 1.0, lightgrey),
                          ('BOX'      , (0,0), (-1,-1), 1.0, lightgrey) ]))
  return doc.build([wm, t], onFirstPage=fix_page_layout, onLaterPages=fix_page_layout)

def main():
  args = docopt(__doc__, version='qrlabels 0.1')
  global verbose; verbose = args['-v']
  ids = args['-i']
  if args['-i']:
    ids = args['-i']
  else:
    save_pdf(args['-p'], 7, 12, 16, 'test.pdf')
  out = args['-o']
