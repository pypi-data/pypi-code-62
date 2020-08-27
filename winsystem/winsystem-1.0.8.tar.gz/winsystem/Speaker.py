import win32com.client
global api
api=win32com.client.Dispatch("SAPI.SpVoice")
def TTStalk(word):
    return api.Speak(str(word))
def Pause():
    return api.Pause()
def Resume():
    return api.Resume()

