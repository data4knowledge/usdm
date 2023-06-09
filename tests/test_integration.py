import json
from src.usdm_excel import USDMExcel

def run_test(filename):
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result = excel.to_json()

  # Useful if you want to see the results. Normally comment out
  #with open(f"tests/integration_test_files/{filename}.json", 'w', encoding='utf-8') as f:
  #  f.write(json.dumps(json.loads(result), indent=2))
  
  with open(f"tests/integration_test_files/{filename}.json", 'r') as f:
    expected = json.dumps(json.load(f)) # Odd, but doing it for consistency of processing
  assert result == expected

def run_test_ne(filename):
  excel = USDMExcel(f"tests/integration_test_files/{filename}.xlsx")
  result_n, result_e = excel.to_nodes_and_edges()

  # Useful if you want to see the results. Normally comment out
  #with open(f"tests/integration_test_files/{filename}_n.json", 'w', encoding='utf-8') as f:
  #  f.write(json.dumps(result_n, indent=2))
  #with open(f"tests/integration_test_files/{filename}_e.json", 'w', encoding='utf-8') as f:
  #  f.write(json.dumps(result_e, indent=2))
  
  with open(f"tests/integration_test_files/{filename}_n.json", 'r') as f:
    expected = json.load(f)
  assert result_n == expected
  with open(f"tests/integration_test_files/{filename}_e.json", 'r') as f:
    expected = json.load(f)
  assert result_e == expected

def test_simple_1():
  run_test('simple_1')

def test_simple_1_ne():
  run_test_ne('simple_1')

def test_config_1():
  run_test('config_1')

def test_config_2():
  run_test('config_2')

def test_no_activity_sheet():
  run_test('no_activity_sheet')

def test_address_comma():
  run_test('address')

def test_complex_1():
  run_test('complex_1')

def test_complex_1_ne():
  run_test_ne('complex_1')
