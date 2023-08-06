from typing import Dict

import numpy as np
import pandas as pd

from houseregression_model import __version__ as _version
from houseregression_model.config.core import config
from houseregression_model.processing.utility_functions import load_pipeline
from houseregression_model.processing.validation import validate_inputs

pipeline_file = f"{config.app_config.pipeline_save_file}{_version}.pkl"
pipe = load_pipeline(file_name=pipeline_file)


def make_predictions(*, input_data: pd.DataFrame) -> Dict:
    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)

    print(validated_data.shape)

    results = {"predictions": [], "version": _version, "errors": errors}

    if not errors:
        predictions = pipe.predict(X=validated_data)

        results = {
            "predictions": [np.exp(val) for val in predictions],
            "version": _version,
            "errors": errors,
        }
    return results
