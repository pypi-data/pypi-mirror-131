from io import BytesIO

from camel_model.camel_model import CamelModel


class NewDistributionImage(CamelModel):
    file_name: str
    file: BytesIO

