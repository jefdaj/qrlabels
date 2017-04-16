qrlabels
========

Generates PDFs of QR codes to print on labels.
See the [examples]() for input and output formats.

```
Usage:
  qrlabels [-v] [-p <prefix>] (-i <idlist> | -n <number>) [-h <history>] [-o <outdir>]

Options:
  -v            Print debugging messages to stdout [defualt: False]
  -p <prefix>   Text to append the UUIDs to, for example "knlab/jj/". [default: ]
  -i <idlist>   List of UUIDs to generate QR codes for
  -n <number>   Number of UUIDs to generate
  -h <history>  Append UUIDs to a history file to prevent accidental repeats
  -o <outdir>   Where to write the QR code images [default: .]
```
