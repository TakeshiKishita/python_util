from abc import ABCMeta


class Reader(metaclass=ABCMeta):
    """
    動画読み込みの、抽象基底クラス
    """
    def open(self):
        """
        読み取り機能を開く
        """
        pass

    def read(self):
        """
        イメージを取得し続ける
        """
        pass

    def close(self):
        """
        処理を終了する
        """
        pass