#!/usr/bin/env python

# TODO figure out lingering margin issues:
#      - when size margins made really big, bottom increases too
#      - nrow = 1 or 20 expands to two pages

# TODO add features:
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
  qrlabels [-v] -p <prefix> -c <nchar> -t <top> -l <left> [-r <right>] [-b <bottom>] -q <qrsize> --nrow <rows> --ncol <cols> <pdfpath>
  qrlabels --help

Options:
  --help        Show this text
  -v            Print debugging messages to stdout [defualt: False]
  -p <prefix>   Text to append the UUIDs to, for example "http://my.site/qrcode/"
  -c <nchar>    Number of characters in the random portion of each QR code
  -t <top>      Top    margin in inches
  -l <left>     Left   margin in inches
  -r <right>    Right  margin in inches (defaults to matching the left)
  -b <bottom>   Bottom margin in inches (defaults to matching the top)
  -q <qrsize>   Height and width of each QR code in inches
  --nrow <rows>  How many rows    of QR codes per page
  --ncol <cols>  How many columns of QR codes per page
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

def qrcode(args):
  text = args['prefix'] + uuid()[:args['nchar']]
  if args['verbose']: print text
  return QrCodeWidget(text)

def qrcodes(args):
  rows = []
  for r in range(1, args['nrow']+1):
    row = []
    for c in range(1, args['ncol']+1):
      widget = qrcode(args)
      bounds = widget.getBounds()
      label  = Drawing(args['qrsize'], args['qrsize'],
                       transform=[args['qrsize']/bounds[2], 0, 0,
                                  args['qrsize']/bounds[3], 0, 0])
      label.add(widget)
      row.append(label)
    rows.append(row)
  return rows

def table(doc, style, args):
  data = qrcodes(args)
  label_widths  = [doc.width  / args['ncol']] * args['ncol']
  label_heights = [(doc.height - style.leading) / args['nrow']] * args['nrow']
  tbl = Table(data, colWidths=label_widths, rowHeights=label_heights,
              hAlign='CENTER', vAlign='MIDDLE')
  tbl.setStyle(TableStyle([ ('ALIGN'    , (0,0), (-1,-1), 'CENTER'),
                            ('VALIGN'   , (0,0), (-1,-1), 'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 1.0, lightgrey),
                            ('BOX'      , (0,0), (-1,-1), 1.0, lightgrey) ]))
  return tbl

def kludge(canvas, doc):
  frame = doc.pageTemplates[0].frames[0]
  frame.leftPadding   = 0
  frame.rightPadding  = 0
  frame.topPadding    = 0
  frame.bottomPadding = 0
  canvas.saveState()

def pdf(args):
  style = getSampleStyleSheet()['Normal']
  cmd = Paragraph(' '.join(['qrlabels']+argv[1:]), style)
  doc = SimpleDocTemplate(pdfpath, pagesize=letter,
                          rightMargin  = args['right'],
                          leftMargin   = args['left',
                          topMargin    = args['top'] - style.leading,
                          bottomMargin = args['bottom'])
  t = table(doc, style, args)
  return doc.build([cmd, t], onFirstPage=kludge, onLaterPages=kludge)

def parse(args):
  top     = args['-t']
  left    = args['-l']
  right   = args['-r']
  bottom  = args['-b']
  if not right : right  = left
  if not bottom: bottom = top
  return {
    'verbose' : args['-v'],
    'prefix'  : args['-p'],
    'top'     : float(top)    * inch,
    'left'    : float(left)   * inch,
    'right'   : float(right)  * inch,
    'bottom'  : float(bottom) * inch,
    'qrsize'  : float(args['-q']) * inch,
    'nchar'   : int(args['-c']),
    'ncol'    : int(args['--ncol']),
    'nrow'    : int(args['--nrow']),
    'pdfpath' : args['<pdfpath>']
  }

def main():
  pdf(parse(docopt(__doc__, version='qrlabels 0.1')))
