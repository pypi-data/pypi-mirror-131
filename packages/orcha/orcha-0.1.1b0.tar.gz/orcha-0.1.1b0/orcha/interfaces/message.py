from dataclasses import dataclass, field

# from typing import Union


@dataclass(order=True)
class Message:
    # priority: Union[int, float] = field()
    id: int = field(compare=False)
    extras: dict = field(compare=False)
