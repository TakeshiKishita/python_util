from abc import ABCMeta


class Reader(metaclass=ABCMeta):
    """
    動画読み込みの、抽象基底クラス
    """
    def open(self, **kwargs):
        """
        読み取り機能を開く
        """
        pass

    def read(self, **kwargs):
        """
        フレームを取得する
        """
        pass

    def close(self, **kwargs):
        """
        処理を終了する
        """
        pass
