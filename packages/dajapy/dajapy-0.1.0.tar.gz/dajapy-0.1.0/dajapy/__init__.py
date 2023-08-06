__version__ = '0.1.0'

from .shareka import Shareka


def is_dajare(sentence: str, kaburi_count=2) -> bool:
    """入力文章がダジャレかどうか判定

    Args:
        sentence (str): ダジャレ判定する文
        kaburi_count (int, optional): ダジャレと判定される重複文字数. Defaults to 2.
            例）kaburi_count=3のとき、
                ハエは速え～ -> ダジャレじゃない
                カエルが帰る -> ダジャレ！

    Returns:
        bool: [description]

    Example:
        >>> is_dajare("ハエは速え～", 2)
        True
        >>> is_dajare("ハエは速え～", 3)
        False
    """
    share = Shareka(
        sentence=sentence,
        kaburi=kaburi_count)
    share.divide()
    share.evaluate()
    is_dajare = share.to_dict()["is_dajare"]

    # 標準出力
    if is_dajare: 
        print("それダジャレ！")
    else:
        print("ダジャレじゃない……")

    return is_dajare
