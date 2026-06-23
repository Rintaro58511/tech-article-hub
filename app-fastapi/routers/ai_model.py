import pickle
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
MODEL_PATH = CURRENT_DIR / "trained_model.pkl"

with open(MODEL_PATH, 'rb') as f:
    loaded_model = pickle.load(f)

def categorize_ai(title: str) -> str:

    """
    Qiita記事のタイトルからカテゴリを自動分類する関数

    Args:
        title (str): 記事のタイトル

    Returns:
        str: 予測されたカテゴリ名（Python, AWS, AWS等）
    """

    return loaded_model.predict([title])[0]