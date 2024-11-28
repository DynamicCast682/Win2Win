from pydantic import BaseModel


class VideoShape(BaseModel):
  width: int
  height: int