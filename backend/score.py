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
    TYPE_ERROR = 5
    INVALID_ID = 6

    @staticmethod
    def warning_message(state: int) -> str:
        if state == ValidateState.INVALID_COLUMN:
            return "カラムが不正です. `id`, `pred` というカラムが含まれているか確認してください."
        elif state == ValidateState.DUPLICATE_ID:
            return "id が重複しています. id はユニークである必要があります."
        elif state == ValidateState.NAN_PRED:
            return "pred に NaN が含まれています."
        elif state == ValidateState.SHAPE_ERROR:
            return "データのサイズが不正です."
        elif state == ValidateState.TYPE_ERROR:
            return "データの型が不正です."
        elif state == ValidateState.INVALID_ID:
            return "id が不正です. テストデータの id と一致しているか確認してください."
        else:
            return "Unknown error."


def validate(submit: pd.DataFrame) -> bool:
    label = pd.read_csv(Constants.LABEL_PATH)

    if submit.shape != label.shape:
        return ValidateState.SHAPE_ERROR

    if (not Constants.ID_COL in submit.columns) or (not Constants.PRED_COL in submit.columns):
        return ValidateState.INVALID_COLUMN

    if len(submit[Constants.ID_COL].unique()) != len(submit):
        return ValidateState.DUPLICATE_ID

    if submit[Constants.PRED_COL].isnull().sum() > 0:
        return ValidateState.NAN_PRED
    
    if label[Constants.LABEL_COL].dtype != submit[Constants.PRED_COL].dtype:
        return ValidateState.TYPE_ERROR

    if not np.all(label[Constants.ID_COL] == submit[Constants.ID_COL]):
        return ValidateState.INVALID_ID
    
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
