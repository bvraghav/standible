## Exports
## ====================================================
__all__ = [
  'read_json', 'write_data', 'read_ndjson'
]

## Json Reader
## ====================================================

def read_json(path) :
  from pathlib import Path
  import json

  with Path(path).open('r') as J :
    data = json.load(J)

  return data

## Output
## ====================================================

def write_data(data, outpath) :
  from pathlib import Path
  import sys

  if str(outpath) == '-' :
    return write_data_stream(data, sys.stdout)

  with Path(outpath).open('w') as F :
    result = write_data_stream(data, F)

  return result

def write_data_stream(data, outstream) :
  import json

  outstream.write('\n'.join(
    json.dumps(record) for record in data
  ))

  outstream.write('\n')


## Read NdJson
## ====================================================

def read_ndjson(path) :
  from pathlib import Path
  import json

  with Path(path).open('r') as Nj :
    data = [
      json.loads(line)
      for line in Nj.readlines()
    ]

  return data
