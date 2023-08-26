from src.usdm_excel.cross_ref import *

class CRTest():

  def __init__(self, id, name):
    self.id = id
    self.name = name

def test_create():
  object = CrossRef()
  assert len(object.references.keys()) == 0
  assert object.references == {}

def test_add():
  item = CRTest(id="1234", name="name")
  cross_references.references = {}
  cross_references.add("name", item)
  assert len(cross_references.references.keys()) == 1
  assert cross_references.references["CRTest.name"] == item

def test_get():
  item = CRTest(id="1234", name="name")
  cross_references.references = {}
  cross_references.references["CRTest.name"] = item
  assert cross_references.get(CRTest, "name") == item

def test_clear():
  item = CRTest(id="1234", name="name")
  cross_references.references = {}
  cross_references.references["CRTest.name"] = item
  assert len(cross_references.references.keys()) == 1
  cross_references.clear()
  assert len(cross_references.references.keys()) == 0
