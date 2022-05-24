import ffmpeg


def convert(inp, out):
    stream = ffmpeg.input(inp)
    x = ffmpeg.output(stream, out)
    ffmpeg.run(x)


convert('test.webm', 'testmodule.mp3')
