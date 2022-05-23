import pafy
import time


def get_res(res):
    x = res.split('x')
    return x[1]


def mycb(total, recvd, ratio, rate, eta):
    print(total, recvd, ratio, rate, eta)


vid = pafy.new("https://www.youtube.com/watch?v=wR0yaeGk3JU")


def vs():
    srm = vid.streams

    l = []
    d = {}
    # Show to users:
    for i in srm:
        ex = i.extension
        res = get_res(i.resolution)
        l.append((ex, res))
        d[(ex, res)] = i

    cnt = 0
    for i in l:
        cnt += 1
        print(cnt, i)

    print(d)

    ch = int(input("Enter: "))

    ch = l[ch - 1]
    print("Your Choice: ", ch)

    stream = d[ch]
    print("Stream downloaded will be: ", stream)

    x = stream.download(quiet=True, callback=mycb)
    print(True)


def aud():
    srm = vid.getbestaudio()
    print(srm)
    srm.download(filepath=r"C:\Users\91982\Desktop\Docs")


# aud()
vs()
