from .filters_base_sch import FilterBase
from pydantic import  ConfigDict

class FilterRead(FilterBase):
    pass

    model_config = ConfigDict(from_attributes=True)