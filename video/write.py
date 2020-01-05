from abc import ABCMeta


class Writer(metaclass=ABCMeta):
    """
    動画書き込みの、抽象基底クラス
    """
    def open(self, **kwargs):
        """
        書き込み機能を開く
        """
        pass

    def write(self, **kwargs):
        """
        出力する
        """
        pass

    def close(self, **kwargs):
        """
        処理を終了する
        """
        pass
