#!/usr/bin/env python

# see www.blog.pythonlibrary.org/2013/03/25/reportlab-how-to-create-barcodes-in-your-pdfs-with-python/
# TODO remove the idlist option? or finish it?
# TODO remove the history option? or finish it?
# TODO multiple pages at once
# TODO add flags for each dimension i ended up with
# TODO rename something more obvious, like qrgen or qrpage or qrcode-stickers
# TODO instead of outdir, use an outpdf
# TODO see if going even smaller helps with the small tubes (less curvature)
# TODO put in terms of actual size, not formula based on a circle (since you might want smaller)
# TODO is there enough space to use full URLs? that would be kinda cool
# TODO add a printout of the prefix, dimensions on the page too, and a watermark :D
# TODO option to print pairs of codes for lid/side of things (boxed together)
# TODO verbose should print the codes as it generates them
# TODO use only lowercase?

# Print on the breakroom iMac with 100% scale
# settings for 3/8" SPOT-1000 labels: 0.50" margins, 0.25" spots, 12 cols, 16 rows
# settings for 1/2" SPOT-2000 labels: 0.45" margins, 0.50" spots, 12 cols, 16 rows
# actually the .45 one seems to work fine for both

# any qr size .30-.35 works great with spot-2000 on white boxes
# 0.18 seems optimal for spot-1000 on the sides of 200uL tubes (trickiest location)

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
  # TODO and add to the history list? or remove that?
  return qr.QrCodeWidget(prefix + uuid()[:nchar])

def fix_page_layout(canv, doc):
  # TODO does this need adjusting for the other pages?
  frame = doc.pageTemplates[0].frames[0]
  frame.leftPadding=frame.rightPadding=frame.topPadding=frame.bottomPadding=0
  canv.saveState()

def save_pdf(prefix, nchar, ncol, nrow, filename):
  # TODO also add multiple pages
  # TODO are l/r, t/b always the same? use one flag if so
  s = getSampleStyleSheet()['Normal']
  wm = Paragraph(' '.join(['qrlabels']+argv[1:]), s)
  doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=0.45*inch, leftMargin=0.45*inch,
                          topMargin=0.45*inch-s.leading, bottomMargin=0.45*inch)
  # TODO reasonable variable names
  qw = doc.width  / ncol
  qh = (doc.height - s.leading) / nrow
  rws = [qw] * ncol
  rhs = [qh] * nrow
  # ls  = sqrt(2) * (0.35/2) * inch # width/height of a square that will fit inside the circle
  ls = 0.18 * inch

  rows = []
  for r in range(1, nrow+1):
    row = []

    # TODO remove, or make this a flag for testing?
    # ls += 0.01 * inch

    for c in range(1, ncol+1):

      qrcode = generate_qrcode(prefix, nchar)
      bounds = qrcode.getBounds()
      width  = bounds[2]
      height = bounds[3]
      label  = Drawing(ls, ls, transform=[ls/width, 0, 0, ls/height, 0, 0])
      label.add(qrcode)
      row.append(label)
    rows.append(row)

  # TODO generate the innergrid to do pairs (or any size group?)
  t = Table(rows, colWidths=rws, rowHeights=rhs, hAlign='CENTER', vAlign='MIDDLE')
  t.setStyle(TableStyle([ ('ALIGN'    , (0,0), (-1,-1), 'CENTER'),
                          ('VALIGN'   , (0,0), (-1,-1), 'MIDDLE'),
                          ('INNERGRID', (0,0), (-1,-1), 1.0, lightgrey),
                          ('BOX'      , (0,0), (-1,-1), 1.0, lightgrey) ]))
  # TODO factor this out into a doc function
  return doc.build([wm, t], onFirstPage=fix_page_layout, onLaterPages=fix_page_layout)

def main():
  args = docopt(__doc__, version='qrlabels 0.1')
  global verbose; verbose = args['-v'] # TODO need to cast as boolean?
  ids = args['-i']
  if args['-i']:
    ids = args['-i']
  else:
    # 6 letters seems to be enough for actual printed QR codes, but not enough
    # for data points from large files. No need for those yet I guess.
    save_pdf(args['-p'], 7, 12, 16, 'test.pdf')
  out = args['-o']
