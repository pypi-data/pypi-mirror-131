import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from houseregression_model import __version__ as _version
from houseregression_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config


def load_dataset(*, filename: str) -> pd.DataFrame:
    """Function to lead the dataset"""

    df = pd.read_csv(Path(f"{DATASET_DIR}/{filename}"))
    df["MSSubClass"] = df["MSSubClass"].astype("O")

    # renaming variables
    transformed = df.rename(columns=config.model_config.variables_to_rename)
    return transformed


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline, saves the versioned model and overwrites any
    previous saved models"""

    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """Remove old model pipelines."""

    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
