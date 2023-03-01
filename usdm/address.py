from .api_base_model import ApiBaseModel
from .code import Code

class Address(ApiBaseModel):

  text: str
  line: str
  city: str
  district: str
  state: str
  postalCode: str
  country: Code

  @classmethod
  def add_address(cls, id, line, city, district, state, postal_code, country):
    text = "%s, %s, %s, %s, %s, %s" % (line, city, district, state, postal_code, country.decode)
    return Address(addressId=id, text=text, line=line, city=city, district=district, state=state, postalCode=postal_code, country=country)