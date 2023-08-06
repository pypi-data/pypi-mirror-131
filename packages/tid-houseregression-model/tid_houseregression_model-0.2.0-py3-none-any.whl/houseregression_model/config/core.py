from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, validator
from strictyaml import YAML, load

import houseregression_model

PACKAGE_ROOT = Path(houseregression_model.__file__).parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"


class AppConfig(BaseModel):
    """Application level config"""

    package_name: str
    training_data_file: str
    test_data_file: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """

    target: str
    variables_to_rename: Dict
    features: List[str]
    test_size: float
    random_state: int
    alpha: float
    learning_rate: float
    n_estimators: int
    categorical_vars_with_na_frequent: List[str]
    categorical_vars_with_na_missing: List[str]
    numerical_vars_with_na: List[str]
    temporal_vars: List[str]
    ref_var: str
    numericals_log_vars: List[str]
    binarize_vars: List[str]
    qual_vars: List[str]
    exposure_vars: List[str]
    finish_vars: List[str]
    garage_vars: List[str]
    categorical_vars: List[str]
    qual_mappings: Dict[str, int]
    exposure_mappings: Dict[str, int]
    garage_mappings: Dict[str, int]
    finish_mappings: Dict[str, int]

    allowed_loss_functions: List[str]
    loss: str

    @validator("loss")
    def allowed_loss_values(cls, v, values, **kwargs):
        """validator to validate right loss function"""

        allowed_values = values.get("allowed_loss_functions")
        if v not in allowed_values:
            raise ValueError(
                f"the loss parameter specified: {v}, "
                f"is not in the allowed set: {allowed_values}"
            )
        return v


class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """Locate the config file path"""

    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise FileNotFoundError(f"Config file not found at {CONFIG_FILE_PATH}")


def fetch_config_from_yaml(config_file_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration. """

    if not config_file_path:
        cfg_path = find_config_file()
    else:
        cfg_path = config_file_path

    if cfg_path:
        with open(cfg_path, "r") as config_file:
            parsed_config = load(config_file.read())
            return parsed_config


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""

    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data),
    )
    return _config


config = create_and_validate_config()
