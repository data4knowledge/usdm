import os
import argparse
import logging

import glob, os

DIR = 'src/usdm_excel/data/'

def file_delete(pattern):
  try:
    for f in glob.glob(os.path.join(DIR, pattern)):
      print(f"FILE1: {f}")
      if f not in [f"{DIR}cdisc_ct_config.yaml"]:
        print(f"FILE2: {f}")
        os.remove(f)
  except Exception as e:
    print(f"Exception '{e}' deleteing file {pattern}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='USDM CDISC Data Preparation',
    description='Builds CDISC BC abd CT load files',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument("--delete", action="store_true", help="Delete the current CT and BC files") 
  parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
  args = parser.parse_args()
  delete = args.delete
  debug = args.debug
  level = logging.DEBUG if debug else logging.INFO

  print(f"DELETE: {delete}")
  print(f"DEBUG: {debug} {level}")
  log = logging.basicConfig(level=level)
  if delete:
    file_delete("cdisc_bcs.yaml")
    file_delete("cdisc_ct*.yaml")
  
  from usdm_excel.cdisc_ct_library import cdisc_ct_library
  from usdm_excel.cdisc_biomedical_concept import cdisc_bc_library