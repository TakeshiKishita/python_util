from abc import ABCMeta


class Writer(metaclass=ABCMeta):
    """
    動画書き込みの、抽象基底クラス
    """
    def open(self):
        """
        書き込み機能を開く
        """
        pass

    def write(self):
        """
        出力する
        """
        pass

    def close(self):
        """
        処理を終了する
        """
        pass
