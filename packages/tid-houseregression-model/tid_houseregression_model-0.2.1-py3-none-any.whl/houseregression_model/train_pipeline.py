import logging

import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from houseregression_model.config.core import config
from houseregression_model.pipeline import price_pipe
from houseregression_model.processing.utility_functions import (
    load_dataset,
    save_pipeline,
)

logging.basicConfig(level=logging.INFO)


def run_training() -> None:
    """
    Training the price model
    """
    data = load_dataset(filename=config.app_config.training_data_file)

    # split the the data in train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    # creating the log of target
    y_train = np.log(y_train)

    # fit the model

    price_pipe.fit(X_train, y_train)

    # scoring the model

    predictions = price_pipe.predict(X_test)
    rscore = r2_score(y_true=np.log(y_test), y_pred=predictions)
    rmse = mean_squared_error(y_true=y_test, y_pred=np.exp(predictions), squared=False)

    logging.info(f"R2 scode is {rscore} and RMSE is {rmse}")

    # save the file

    save_pipeline(pipeline_to_persist=price_pipe)


if __name__ == "__main__":
    run_training()
