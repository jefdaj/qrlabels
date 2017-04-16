qrlabels
========

Generates PDFs of QR codes to print on labels. See the
[examples](https://github.com/jefdaj/qrlabels/tree/master/examples) for input
and output formats.

```
Usage:
  qrlabels [-v] -p <prefix> <pdfpath>
  qrlabels --help

Options:
  --help        Show this text
  -v            Print debugging messages to stdout [defualt: False]
  -p <prefix>   Text to append the UUIDs to, for example "http://my.site/qrcode/"
     <pdfpath>  Where to write the QR code images
```

Make sure to use the highest quality print settings when printing small codes;
it makes a large difference in readability on smartphones.

Things I plan to implement eventually:

* Keep a history file of used QR codes to avoid accidental repeats
* Accept a list of codes from a file rather than generating them
* Print multiple pages at once

Things I probably won't bother to implement, but would still happily merge:

* Accept units other than inches
* Just about anything useful
