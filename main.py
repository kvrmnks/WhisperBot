import tkinter
import json, requests
import pandas as pd
from tkinter.filedialog import askopenfilename
import os

# authKey qq url group
log = {}


def init():
    global log
    if os.path.exists('./log'):
        f = open('./log','r')
        log = json.loads(f.read())
        f.close()
        authKeyInput.insert(tkinter.END, log['authKey'])
        qqInput.insert(tkinter.END, log['qq'])
        urlInput.insert(tkinter.END, log['url'])
        groupInput.insert(tkinter.END, log['group'])
    else:
        pass


def save():
    global log
    log['authKey'] = authKeyInput.get()
    log['qq'] = qqInput.get()
    log['url'] = urlInput.get()
    log['group'] = groupInput.get()
    f = open('./log','w')
    f.write(json.dumps(log))
    f.close()


def post(url, data):
    data = json.dumps(data)
    r = requests.post(urlInput.get() + url, data)
    return json.loads(r.text)


def getSession():
    global sessionKey
    t = post('/auth', {'authKey': authKeyInput.get()})
    print(t)
    logText.insert(tkinter.END, str(t) + '\n')
    sessionKey = t['session']

    t2 = post('/verify', {'sessionKey': t['session'], 'qq': qqInput.get()})
    print(t2)
    logText.insert(tkinter.END, str(t2) + '\n')
    save()
    pass


def includeQQList():
    global QQList
    io = askopenfilename()
    data = pd.read_table(io, header=None)
    print(data[0].tolist())
    QQList = data[0].tolist()

    pass


def checkQQList():
    moreTk = tkinter.Tk()
    table = tkinter.Listbox(moreTk)
    table.pack()
    for i in QQList:
        table.insert(tkinter.END, i)
    moreTk.mainloop()


def send():
    save()
    msg = contentText.get('1.0', tkinter.END)
    for i in QQList:
        t = post('/sendTempMessage', {
            'sessionKey': sessionKey,
            'qq': i,
            'group': groupInput.get(),
            'messageChain': [
                {'type': 'Plain', 'text': msg}
            ]
        })
        logText.insert(tkinter.END, str(t) + '\n')
    # print(contentText.get('1.0',tkinter.END))
    pass


QQList = []
sessionKey = ''

tk = tkinter.Tk()
urlLabel = tkinter.Label(tk, text='输入url')
urlInput = tkinter.Entry(tk)

authKeyLabel = tkinter.Label(tk, text='输入authKey')
authKeyInput = tkinter.Entry(tk)
qqLabel = tkinter.Label(tk, text='输入QQ')
qqInput = tkinter.Entry(tk)
authKeyButton = tkinter.Button(tk, text='确认', command=getSession)

logText = tkinter.Text(tk, width=30, height=15)

groupLabel = tkinter.Label(tk, text='输入群号')
groupInput = tkinter.Entry(tk)
memberListButton = tkinter.Button(tk, text='导入发送人员QQ号', command=includeQQList)
memberListLook = tkinter.Button(tk, text='查看导入人员QQ号', command=checkQQList)
contentText = tkinter.Text(tk, width=30, height=15)
sendButton = tkinter.Button(tk, text='发送', command=send)


def layout():
    urlLabel.pack()
    urlInput.pack()

    authKeyLabel.pack()
    authKeyInput.pack()
    qqLabel.pack()
    qqInput.pack()
    authKeyButton.pack()

    logText.pack()
    groupLabel.pack()
    groupInput.pack()
    memberListButton.pack()
    memberListLook.pack()
    contentText.pack()
    sendButton.pack()


if __name__ == '__main__':
    layout()
    init()
    tk.mainloop()
