import subprocess as sp
from read import Reader
from logging import getLogger


class StreamingWriter(Reader):
    def __init__(self):
        self.logger = getLogger(__name__)
        self.video_writer = None
        self.input = None
        self.output = None

    def open(self, video_input, video_output, frame_size, fps=None):

        self.input = video_input
        self.output = video_output

        width, height = frame_size
        frame_rate = f'-r {fps}' if fps else '-re'
        cmd = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{width}x{height}',
            '-px_fmt', 'bgr24',
            frame_rate,
            '-i', '-',
            '-an',
            'pix_fmt', 'yuv420p',
            '-threads', '0',
            '-f', 'v4l2',
            self.output
        ]

        self.proc = sp.Popen(cmd, stdin=sp.PIPE)

    def write(self, image):
        self.proc.stdin.write(image.tostring())

    def close(self):
        self.proc.kill()
        pass
