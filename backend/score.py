import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

from const import Constants
from typing import Tuple, Union

class ValidateState:
    VALID = 0
    INVALID_COLUMN = 1
    DUPLICATE_ID = 2
    NAN_PRED = 3
    SHAPE_ERROR = 4

    @staticmethod
    def warning_message(state: int) -> str:
        if state == ValidateState.INVALID_COLUMN:
            return "Invalid column"
        elif state == ValidateState.DUPLICATE_ID:
            return "Duplicate id"
        elif state == ValidateState.NAN_PRED:
            return "Nan in pred"
        elif state == ValidateState.SHAPE_ERROR:
            return "Shape error"
        else:
            return "Unknown error"


def validate(df: pd.DataFrame) -> bool:
    label = pd.read_csv(Constants.LABEL_PATH)

    if df.shape != label.shape:
        return ValidateState.SHAPE_ERROR

    if (not Constants.ID_COL in df.columns) or (not Constants.PRED_COL in df.columns):
        return ValidateState.INVALID_COLUMN

    if len(df[Constants.ID_COL].unique()) != len(df):
        return ValidateState.DUPLICATE_ID

    if df[Constants.PRED_COL].isnull().sum() > 0:
        return ValidateState.NAN_PRED

    return ValidateState.VALID



def load_public_private_setting() -> Tuple[np.ndarray, np.ndarray]:
    public_private_setting = pd.read_csv(Constants.PUBLIC_PRIVATE_SETTING)
    public_mask = public_private_setting["setting"] == "public"
    private_mask = public_private_setting["setting"] == "private"
    assert np.logical_or(public_mask, private_mask).all()

    return public_mask.values, private_mask.values


def public_and_private_score(
    y_true: np.ndarray, y_pred: np.ndarray, public_mask: Union[np.ndarray, None] = None
) -> np.float64:
    if public_mask is None:
        public_mask, _ = load_public_private_setting()

    public_score = Constants.score(
        y_true=y_true[public_mask],
        y_pred=y_pred[public_mask],
    )

    private_score = Constants.score(
        y_true=y_true[~public_mask],
        y_pred=y_pred[~public_mask],
    )

    return public_score, private_score
