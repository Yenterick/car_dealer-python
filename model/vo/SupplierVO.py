from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Callable

@dataclass
class SupplierVO:
    supplier_id: int | None
    name: str
    email: str
    phone: str
    created_at: datetime = field(default=datetime.now())

    # ====== LAZY LOADING  ======

    _buys_loader: Callable[[], List['BuyVO']] | None = field(default=None, repr=False) # type: ignore
    _buys_cache: List['BuyVO'] | None = field(default=None, repr=False) # type: ignore

    _cars_loader: Callable[[], List['CarVO']] | None = field(default=None, repr=False) # type: ignore
    _cars_cache: List['CarVO'] | None = field(default=None, repr=False) # type: ignore

    _spares_loader: Callable[[], List['SpareVO']] | None = field(default=None, repr=False) # type: ignore
    _spares_cache: List['SpareVO'] | None = field(default=None, repr=False) # type: ignore

    @property
    def buys(self) -> List['BuyVO']: # type: ignore
        if self._buys_cache is None and self._buys_loader is not None:
            self._buys_cache = self._buys_loader()
        return self._buys_cache # type: ignore

    @property
    def cars(self) -> List['CarVO']: # type: ignore
        if self._cars_cache is None and self._cars_loader is not None:
            self._cars_cache = self._cars_loader()
        return self._cars_cache # type: ignore

    @property
    def spares(self) -> List['SpareVO']: # type: ignore
        if self._spares_cache is None and self._spares_loader is not None:
            self._spares_cache = self._spares_loader()
        return self._spares_cache # type: ignore
    
    '''
    Needed to add the type ignore comment to all the VOs bc Pylance typechecker
    won't detect them but if we import them they will make a circular import
    '''