class Volume():
    def setTela(otela):
        global tela 
        tela = otela

    #Controle do volume
    def volumeMaisHandler():
        print(tela)
        newPos = tela.pgsVolume.value() + 2
        tela.pgsVolume.setValue(newPos)
        tela.wVolume.setVisible(True)
        tela.timerBarraVolume.start(2000)

    def volumeMenosHandler():
        newPos = tela.pgsVolume.value() - 2
        tela.pgsVolume.setValue(newPos)
        tela.wVolume.setVisible(True)
        tela.timerBarraVolume.start(2000)        

    #Barra volume visible off
    def barraVolumeOff():
        tela.wVolume.setVisible(False)
        tela.timerBarraVolume.stop()

    #BtnMude
    def mutehandler():
        print("mute aqui")