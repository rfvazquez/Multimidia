import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
#import RPi.GPIO as GPIO

class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()
    

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Principal.ui', self)

        #Variáveis utilizadas no funcionamento do sistema
        self.volume = 0
        self.userAction = -1 
        
        #Colocando os paineis como nao visivel
        self.wPlayer.setVisible(False)
        self.wVolume.setVisible(False)
        self.wConfiguracoes.setVisible(False)
        self.wAvisos.setVisible(False)
        
        #Timer para o Relógio e Data
        self.timerBarraVolume = QTimer()
        self.timerBarraVolume.timeout.connect(self.barraVolumeOff)
        self.timerBarraVolume.start(1000)


        #Timer para os sensores
        #self.timerSensores = QTimer()
        #self.timerSensores.timeout.connect(self.ControleVeiculo)
        #self.timerSensores.start(1000)

        #Timer para barra de volume
        self.timer = QTimer()
        self.timer.timeout.connect(self.hora)
        self.timer.start(2000)
        
        
        #Criando o Player de Musica
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        
        self.player.durationChanged.connect(self.updateDuration)
        self.player.positionChanged.connect(self.updatePosition)        

        self.model = PlaylistModel(self.playlist)
        self.listMusic.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlistPositionChanged)
        selection_model = self.listMusic.selectionModel()
        selection_model.selectionChanged.connect(self.playlistSelectionChanged)
        self.player.error.connect(self.erroralert)

        #Muda Imagem DLR Aceso
        self.ckbDLR.stateChanged.connect(self.alteraImagemFarol)
        
        #Click para abrir o player de musica
        self.btnPlayer.clicked.connect(self.telaPlayer)

        #Botão Volume
        self.dialVolume.valueChanged.connect(self.volumehandler)
        
        #Click no botão de MUTE
        self.btnMute.clicked.connect(self.mutehandler)

        #Click para configurações
        self.btnConfig.clicked.connect(self.confighandler)

        #Botão de seleção de arquivos de musica
        self.btnFolder.clicked.connect(self.searchConfigFolder)

        #self.showFullScreen()
        self.show()
        


    def alteraImagemFarol(self):
        if(self.ckbDLR.isChecked()):
            self.lblImagemKa.setPixmap(QPixmap("../Icones/LanternaAcesa.png"))
        else:
            self.lblImagemKa.setPixmap(QPixmap("../Icones/LanternaApagada.png"))



    #Controle do volume
    def volumehandler(self):
        self.wVolume.setVisible(True)
        self.pgsVolume.setValue(self.dialVolume.value())
        self.timerBarraVolume.start(2000)

    #Barra volume visible off
    def barraVolumeOff(self):
        self.wVolume.setVisible(False)
        self.timerBarraVolume.stop()

    #BtnMude
    def mutehandler(self):
        if(self.dialVolume.value() == 0):
            self.dialVolume.setValue(self.volume)
        else:
            self.volume = self.dialVolume.value()
            self.dialVolume.setValue(0)
        
    #Relógio do sistema
    def hora(self):
        now = datetime.now()
        self.lblData.clear();
        self.lblHorario.setText(now.strftime("%H:%M"))
        self.lblData.setText(now.strftime("%d/%m/%Y"))

    #Configurações
    def confighandler(self):
        if(self.wConfiguracoes.isHidden()):
            #self.wConfiguracoes.setVisible(True)
            self.wConfiguracoes.showFullScreen()
        else:
            self.wConfiguracoes.setVisible(False)        


    #Cria o player de musica
    def telaPlayer(self):
        if(self.wPlayer.isHidden()):
            #addFiles local para escolher a midia
            if self.playlist.mediaCount() == 0:
                self.verifyConfigFolder()
            #Botão de play da musica
            self.btnPlay.clicked.connect(self.playhandler)
            self.btnAdiantar.clicked.connect(self.nextSong)
            self.btnVoltar.clicked.connect(self.prevSong)
            self.btnStop.clicked.connect(self.stophandler)
            self.btnRandom.clicked.connect(self.addFiles)
            #Trocando o nome do arquivo que está tocando
            self.playlist.currentMediaChanged.connect(self.songChanged)
            self.wPlayer.setVisible(True)
        else:
            self.wPlayer.setVisible(False)

    def addFiles(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../Icones/Play2.png"), QIcon.Normal, QIcon.Off)
        self.btnPlay.setIcon(icon)          
        if self.playlist.mediaCount() != 0:
            self.playlist.clear()
        self.folderIterator()

    def searchConfigFolder(self):
        folderChosen = QFileDialog.getExistingDirectory(self, 'Selecione local dos Arquivos', '~')
        self.edtLocalArquivos.setText(folderChosen)

    def verifyConfigFolder(self):
        self.folderRotine(self.edtLocalArquivos.text())

    def folderIterator(self):        
        self.folderRotine(QFileDialog.getExistingDirectory(self, 'Selecione local dos Arquivos', '~'))

    def folderRotine(self, folderChosen):
        if folderChosen != None:
            it = QDirIterator(folderChosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
            if(self.playlist.mediaCount() > 0):
                self.model.layoutChanged.emit()
                self.player.play()
                self.player.setPlaylist(self.playlist)
                self.player.playlist().setCurrentIndex(0)
                self.lblMsgPlayer.setText("Arquivos carregados");
            else:
                self.lblMsgPlayer.setText("Nenhum arquivo encontrado");        
        else:
            self.lblMsgPlayer.setText("Processo de carregamento cancelado!");


    def erroralert(self, *args):
        print(args)
    
    def playhandler(self):
        if self.playlist.mediaCount() == 0:
            self.lblMsgPlayer.setText("Nenhum arquivo carregado!")
        elif self.playlist.mediaCount() != 0:
            if(self.userAction == 1):
                icon = QIcon()
                icon.addPixmap(QPixmap("../Icones/Play2.png"), QIcon.Normal, QIcon.Off)
                self.btnPlay.setIcon(icon)
                self.player.pause()
                self.userAction = 2
            else:
                icon = QIcon()
                icon.addPixmap(QPixmap("../Icones/pause2.png"), QIcon.Normal, QIcon.Off)
                self.btnPlay.setIcon(icon)
                self.player.play()
                self.userAction = 1
                            
    def songChanged(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            self.statusbar.showMessage("Tocando - " + url.fileName())

    def prevSong(self):
        if self.playlist.mediaCount() == 0:
            self.lblMsgPlayer.setText("Nenhum arquivo carregado!");
        elif self.playlist.mediaCount() != 0:
            self.player.playlist().previous()
            icon = QIcon()
            icon.addPixmap(QPixmap("../Icones/Play2.png"), QIcon.Normal, QIcon.Off)
            self.btnPlay.setIcon(icon)  
            

    def nextSong(self):
        if self.playlist.mediaCount() == 0:
            self.lblMsgPlayer.setText("Nenhum arquivo carregado!");
        elif self.playlist.mediaCount() != 0:
            self.player.playlist().next()


    def stophandler(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../Icones/Play2.png"), QIcon.Normal, QIcon.Off)
        self.btnPlay.setIcon(icon)        
        self.userAction = 0
        self.player.stop()


    def updateDuration(self, duration):
        self.sldMusicPos.setMaximum(duration)
        if duration >= 0:
            self.lblTempoTotal.setText(convertTempo(duration))

    def updatePosition(self, position):
        if position >= 0:
            self.lblTempoMusica.setText(convertTempo(position))
        self.sldMusicPos.blockSignals(True)
        self.sldMusicPos.setValue(position)
        self.sldMusicPos.blockSignals(False)

    def playlistPositionChanged(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.listMusic.setCurrentIndex(ix)

    def playlistSelectionChanged(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)

    #Final do Player de musica

    #Controle Veiculo
    def ConfiguracaoSistema(self):
        GPIO.setmode(GPIO.BCM)

        #Descrição das portas utilizadas no projeto
        luzExternaOut = 5
        luzInternaOut = 6
        posChaveIn = 13
        portaEsquerdaIn = 19
        portaDireitaIn = 26
        ilumunacaoIn = 21
        cintoIn = 20

        #Leitura de sensores
        gpio.setup(posChaveIn, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        gpio.setup(portaEsquerdaIn, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        gpio.setup(portaDireitaIn, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        gpio.setup(ilumunacaoIn, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        gpio.setup(cintoIn, gpio.IN, pull_up_down = gpio.PUD_DOWN)

        #Saída de comandos
        GPIO.setup(luzExternaOut, GPIO.OUT)
        GPIO.setup(luzInternaOut, GPIO.OUT)


    def verificaLuzPorta(self):
        luzInternaOn = False
        #aqui vamos verificar a luz interna para a porta
        if(self.ckbLuzInternaPorta.isChecked()):
            if((gpio.input(portaEsquerdaIn) == 1) or (gpio.input(portaDireitaIn) == 1)):
                luzInternaOn = True
        return luzInternaOn

    def verificaLuzLanterna(self):
        return ((gpio.input(posChaveIn) == 1) and self.ckbDLR.isChecked())

    def verificaLuzExterna(self):
        return ((gpio.input(posChaveIn) == 1) and self.ckbLuzInternaLanterna.isChecked())

    #função para aviso de Porta
    def verificaAvisoPorta(self):
        if(gpio.input(posChaveIn) == 1):
            if(gpio.input(portaEsquerdaIn) == 1 and gpio.input(portaDireitaIn) == 1):
                self.exibeAviso("Portas abertas", "portas")
            else:
                if(gpio.input(portaEsquerdaIn) == 1):
                    self.exibeAviso("Porta esquerda aberta", "portae")
                else:
                    if(gpio.input(portaDireitaIn) == 1):
                        self.exibeAviso("Porta direita aberta", "portad")
                    else:
                        self.wAvisos.setVisible(False)
        else:
            self.wAvisos.setVisible(False)


    #função para aviso de cinto
    def verificaAvisoCinto():
        if(gpio.input(posChaveIn) == 1):
            if(gpio.input(cintoIn) == 1):
               self.exibeAviso("Por favor, afivele o sinto de segurança", "cinto")
            else:
                self.wAvisos.setVisible(False)
        else:
            self.wAvisos.setVisible(False)
                
    def exibeAviso(self, mensagem, imagem):
        self.lblMensagem.setText(mensagem)
        self.lblImagem.setPixmap(QPixmap("../Icones/"+imagem+".png"))
        self.wAvisos.setVisible(True)

    
    def ControleVeiculo(self):
        #aqui vamos ver a luz externa
        if(self.verificaLuzExterna()):
            gpio.output(luzExternaOut, gpio.HIGH)
        else:
            gpio.output(luzExternaOut, gpio.LOW)
            
        #Aqui vamos ver a luz interna
        if(self.verificaLuzPorta() or self.verificaLuzLanterna()):
            gpio.output(luzInternaOut, gpio.HIGH)
        else:
            gpio.output(luzInternaOut, gpio.LOW)
            
        #Aqui vamos verificar o aviso de cinto
        self.verificaAvisoCinto()
        #aqui vamos ver as mensagens de aviso do carro
        self.verificaAvisoPorta()


    #Fim controle veiculo


#Converte Milisegundos em hh:mm:ss        
def convertTempo(ms):
    h, r = divmod(ms, 36000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%02d:%02d" % (h,s))
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())

main()
