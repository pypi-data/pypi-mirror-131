from typing import List, Optional

from camel_model.camel_model import CamelModel

from xlsx_lib.domain.shared.text_line import TextLine
from xlsx_lib.domain.distribution.distribution_image import DistributionImage


class DataBlock(CamelModel):
    text_lines: Optional[List[TextLine]]
    image: Optional[DistributionImage]
    upper_text: Optional[bool]

