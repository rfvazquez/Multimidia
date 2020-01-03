class Config():
    def setTela(otela):
        global tela 
        tela = otela

    def alteraImagemFarol():
        if(tela.ckbDLR.isChecked()):
            tela.lblImagemKa.setPixmap(QPixmap("Icones/LanternaAcesa.png"))
        else:
            tela.lblImagemKa.setPixmap(QPixmap("Icones/LanternaApagada.png"))

    #Configurações
    def confighandler():
        if(tela.wConfiguracoes.isHidden()): 
            tela.wConfiguracoes.showFullScreen()
        else:
            tela.wConfiguracoes.setVisible(False)  