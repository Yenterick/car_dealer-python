from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Callable

@dataclass
class CustomerVO:
    customer_id: int | None
    dni: str
    name: str
    last_name: str
    created_at: datetime = field(default=datetime.now())

    # ====== LAZY LOADING  ======

    _sales_loader: Callable[[], List['SaleVO']] | None = field(default=None, repr=False) # type: ignore
    _sales_cache: List['SaleVO'] | None = field(default=None, repr=False) # type: ignore

    @property
    def sales(self) -> List['SaleVO']: # type: ignore
        if self._sales_cache is None and self._sales_loader is not None:
            self._sales_cache = self._sales_loader()
        return self._sales_cache # type: ignore

    '''
    Needed to add the type ignore to all the VOs bc Pylance typechecker
    won't detect them but if we import them they will make a circular import
    '''