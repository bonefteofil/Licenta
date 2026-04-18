from sqlmodel import SQLModel, Field


class MembruParcare(SQLModel, table=True):
    __tablename__: str = "membru_parcare" # type: ignore
    
    id: int | None = Field(default=None, primary_key=True)
    parcare_id: int = Field(default=None, foreign_key="parcare.id", ondelete="CASCADE")
    utilizator_id: int = Field(default=None, foreign_key="utilizator.id", ondelete="CASCADE")


class MembruParcareInfo(SQLModel):
    parcare_id: int = Field(default=None, foreign_key="parcare.id")
    utilizator_id: int = Field(default=None, foreign_key="utilizator.id")
