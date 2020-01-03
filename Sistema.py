import sys
from datetime import datetime
from ControleCarro import *
from Player import *
from Volume import *
from Config import *

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
        
        Player.setTela(self)
        Volume.setTela(self)
        Config.setTela(self)

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
        self.timerBarraVolume.timeout.connect(Volume.barraVolumeOff)
        self.timerBarraVolume.start(1000)

        #Timer para os sensores
        #self.timerSensores = QTimer()
        #self.timerSensores.timeout.connect(ControleCarro.testeControleCarro)
        #self.timerSensores.start(1000)

        #Timer para barra de volume
        self.timer = QTimer()
        self.timer.timeout.connect(self.hora)
        self.timer.start(2000)
        
        
        #Criando o Player de Musica
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        
        self.player.durationChanged.connect(Player.updateDuration)
        self.player.positionChanged.connect(Player.updatePosition)        

        self.model = PlaylistModel(self.playlist)
        self.listMusic.setModel(self.model)
        self.playlist.currentIndexChanged.connect(Player.playlistPositionChanged)
        selection_model = self.listMusic.selectionModel()
        selection_model.selectionChanged.connect(Player.playlistSelectionChanged)
        self.player.error.connect(Player.erroralert)

        #Muda Imagem DLR Aceso
        self.ckbDLR.stateChanged.connect(Config.alteraImagemFarol)
        
        #Click para abrir o player de musica
        self.btnPlayer.clicked.connect(Player.telaPlayer)
        
        #Click no botão de MUTE
        self.btnMute.clicked.connect(Volume.mutehandler)
        self.btnVolMais.clicked.connect(Volume.volumeMaisHandler)
        self.btnVolMenos.clicked.connect(Volume.volumeMenosHandler)
        
        #Click para configurações
        self.btnConfig.clicked.connect(Config.confighandler)

        #Botão de seleção de arquivos de musica
        self.btnFolder.clicked.connect(Player.searchConfigFolder)
        
        #self.showFullScreen()
        self.show()
    #Relógio do sistema
    def hora(self):
        now = datetime.now()
        self.lblData.clear();
        self.lblHorario.setText(now.strftime("%H:%M"))
        self.lblData.setText(now.strftime("%d/%m/%Y"))

   


        
          

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())

main()
