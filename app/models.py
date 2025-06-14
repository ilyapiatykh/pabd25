import pandas as pd
from pydantic import BaseModel, field_validator


class Apartment(BaseModel):
    total_meters: int
    rooms_count: int
    floors_count: int
    floor: int

    @field_validator("total_meters", "rooms_count", "floors_count", "floor", mode="after")
    @classmethod
    def is_positive(cls, value: int):
        if value < 1:
            raise ValueError("Must be more than 0")

        return value

    def to_df(self):
        return pd.DataFrame(
            [
                {
                    "total_meters": self.total_meters,
                    "rooms_count": self.rooms_count,
                    "floors_count": self.floors_count,
                    "floor": self.floor,
                }
            ]
        )
