import json

from pydantic import (BaseModel, ConfigDict, Field, ValidationError,
                      model_validator)


class ConfigError(Exception):
    """The config file was given but cannot be used."""
    pass


class Config(BaseModel):
    """Ignore comments later"""
    
    model_config = ConfigDict(extra='forbid', strict=True, frozen=False)

    highscore_filename: str = Field(default='scores', min_length=1)
    levels: int = Field(default=10, ge=1)
    width: int = Field(default=20, ge=5)
    height: int = Field(default=20, ge=5)
    lives: int = Field(default=3, ge=1)
    pacgum: int = Field(default=42, ge=1)
    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)
    seed: int = Field(default=42, ge=0)
    level_max_time: int = Field(default=90, ge=1)
    perfect: bool = Field(default=False)

    @model_validator(mode='after')
    def check_consistency(self) -> 'Config':
        """check if nbr of gums not gonna eat the screen"""
        if self.pacgum > self.width * self.height:
            raise ValueError(
                f"pacgum ({self.pacgum}) cannot exceed "
                f"width * height ({self.width * self.height})")
        return self

    @classmethod
    def from_json_file(cls, filepath: str | None) -> 'Config':
        """No file -> all defaults. File -> missing keys get defaults,
        anything present must be valid, otherwise ConfigError."""
        if filepath is None:
            raise ValueError("Need a json file (setting) to make life good")
            # return cls()
        
        try:
            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, OSError) as e:
            raise ConfigError(
                f"cannot read '{filepath}': {e.strerror}") from e
        except json.JSONDecodeError as e:
            raise ConfigError(
                f"'{filepath}' is not valid JSON "
                f"(line {e.lineno}, column {e.colno}): {e.msg}") from e

        if not isinstance(data, dict):
            raise ConfigError(
                f"'{filepath}': top level must be a JSON object {{...}}")

        try:
            return cls.model_validate(data)
        except ValidationError as e:
            raise ConfigError(f"Somthing went bad odin said : {e}")
