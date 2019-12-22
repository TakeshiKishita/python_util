import subprocess as sp
from read import Reader


class StreamingWriter(Reader):
    def __init__(self, video_input, video_output, frame_size, fps=None):
        self.video_writer = None
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

    def open(self):
        pass

    def write(self, image):
        self.proc.stdin.write(image.tostring())

    def close(self):
        self.proc.kill()
        pass
