import cv2
import time
from logging import getLogger
from multiprocessing import Process, Queue, Array
from read import Reader


class StreamingReader(Reader):
    """
    遅延なく動画を読み込む
    ストリーミング動画の読み込みを想定し、常に最新のフレームを読み込むよう実装している。
    """
    def __init__(self, src):
        """
        初期化
        Args:
            src: 動画を読み取るソース
        """
        self.logger = getLogger(__name__)
        self.src = src

        # 幅, 高さ, フレーム数, フレームレートの初期化
        self.width, self.height, self.frame_num, self.fps = None, None, None, None
        self.queue = None
        self.process = None

    def open(self):
        """
        openCVインスタンスの初期化
        """
        # フレーム情報を取得するための、共有メモリを確保する
        info_array = Array('f', 4)
        # マルチプロセスで、フレームを格納するキューを作成
        self.queue = Queue(maxsize=1)

        # マルチプロセスで、フレームを取得し続ける
        self.process = Process(target=self.get_frame, args=(self.src, self.queue, info_array))
        self.process.start()

        # 共有メモリに書き込まれるのを待ち、フレームの情報を取得する
        time.sleep(5)
        self.width, self.height, self.frame_num, self.fps = info_array

        self.logger.info(
            'width:{}, height:{}, frame_num:{}, fps:{}'.format(self.width, self.height, self.frame_num, self.fps))

    def read(self, timeout=30):
        """
        キューからイメージを取得し続ける
        """
        while True:
            # キューからイメージを取得。できない場合は、最大30秒間ブロッキングが行われる。
            # （この処理の後、キューが空になる）
            bgr_img = self.queue.get(timeout=timeout)

            yield bgr_img

    def close(self):
        """
        処理を終了
        """
        self.process.terminate()
        self.queue.close()

    def __dell__(self):
        self.close()

    def get_frame(self, src, queue, info_array):
        """
        フレームを取得
        キューが空の場合、フレームをキューに入れ続ける
        Args:
            src: opencvで読み込むカメラソース（バイス番号、URL）
            queue:キュー
            info_array: フレーム情報を格納する、共有メモリ配列
        """
        self.logger.info('get_frame start')

        # 動画読み込み
        cap = cv2.VideoCapture(src)

        # フレーム情報を、共有メモリ上に保持する
        info_array[0] = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        info_array[1] = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        info_array[2] = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        info_array[3] = cap.get(cv2.CAP_PROP_FPS)

        try:
            while cap.isOpened():
                # フレームを取得する
                ret, frame = cap.read()

                # フレーム取得に失敗した場合、エラーを出力し、処理を抜ける
                if not ret:
                    self.logger.error('Failed to cv2.VideoCapture.read()')
                    break

                # キューが空の場合、キューにフレームを入れる。
                if queue.empty():
                    queue.put(frame)
        finally:
            if cap.isOpened():
                cap.release()
            self.logger.info('get_frame end')


def _run(source):
    """
    ディスプレイで確認
    """
    # インスタンスの初期化
    c = StreamingReader(source)
    c.open()
    try:
        for frame in c.read():
            # 出力内容をディスプレイに表示
            cv2.imshow('test', frame)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print('pushed Ctrl-C')
    finally:
        # 終了処理
        c.close()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # infoログを表示させたいので、ログレベルを変更
    from logging import basicConfig, INFO
    basicConfig(level=INFO)

    # 入力を設定（動画ではなく、ストリーミングを指定する）
    _run('rtsp://xxxx')
