qrlabels
========

Generates PDFs of QR codes to print on labels. See the
[examples](https://github.com/jefdaj/qrlabels/tree/master/examples) for input
and output formats. And remember to use the highest quality print settings for
readability of small QR codes.

```
Usage:
  qrlabels [-v] -p PREFIX -n NCHAR -m MARGINS -d DIMENSIONS -s SIDE PDFPATH
  qrlabels --help

Options:
  --help         Show this text
  -v             Print the text of each QR code [defualt: False]
  -p PREFIX      Text to start QR codes with, for example "http://my.site/qrcode/"
  -n NCHAR       Number of characters in the random portion of each QR code
  -d DIMENSIONS  Dimensions of the QR codes table in rows and columns,
                 for example "4x6" or "12x16". No spaces!
  -s SIDE        Length of each side of the QR codes. Allowed units: mm, cm, in, px
  -m MARGINS     Comma-separated margins. Specify one, two, or all four:
                 * one  means all margins are equal
                 * two  means top/bottom, left/right
                 * four means top, bottom, left, right
                 Allowed units are mm, cm, in, px. No spaces!
                 Examples: "10mm,20mm" "1in" "25px,25px,20px,20px"
     PDFPATH     Where to save the output PDF
```

Features I plan to implement eventually:

* "Test mode" that prints size information on the paper
* Accept a list of codes from a file rather than generating them
* Groups of repeated barcodes for when you want more than one of each
* Keep a history file of used QR codes to avoid accidental repeats
* Print multiple pages at once
