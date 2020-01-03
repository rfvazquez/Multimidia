from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Player():
#Cria o player de musica
    def setTela(otela):
        global tela 
        tela = otela
        
#Converte Milisegundos em hh:mm:ss        
    def convertTempo(ms):
        h, r = divmod(ms, 36000)
        m, r = divmod(r, 60000)
        s, _ = divmod(r, 1000)
        return ("%02d:%02d" % (h,s))

    def telaPlayer(self):
        print(tela)
        if(tela.wPlayer.isHidden()):
            #addFiles local para escolher a midia
            if tela.playlist.mediaCount() == 0:
                Player.verifyConfigFolder()
            #Botão de play da musica
            tela.btnPlay.clicked.connect(Player.playhandler)
            tela.btnAdiantar.clicked.connect(Player.nextSong)
            tela.btnVoltar.clicked.connect(Player.prevSong)
            tela.btnStop.clicked.connect(Player.stophandler)
            tela.btnRandom.clicked.connect(Player.addFiles)
            #Trocando o nome do arquivo que está tocando
            tela.playlist.currentMediaChanged.connect(Player.songChanged)
            tela.wPlayer.setVisible(True)
        else:
            tela.wPlayer.setVisible(False)

    def addFiles():
        icon = QIcon()
        icon.addPixmap(QPixmap("Icones/Play2.png"), QIcon.Normal, QIcon.Off)
        tela.btnPlay.setIcon(icon)          
        if tela.playlist.mediaCount() != 0:
            tela.playlist.clear()
        tela.folderIterator()

    def searchConfigFolder():
        folderChosen = QFileDialog.getExistingDirectory(tela, 'Selecione local dos Arquivos', '~')
        tela.edtLocalArquivos.setText(folderChosen)

    def verifyConfigFolder():
        print("aqui")
        Player.folderRotine(tela.edtLocalArquivos.text())

    def folderIterator():        
        Player.folderRotine(QFileDialog.getExistingDirectory(tela, 'Selecione local dos Arquivos', '~'))

    def folderRotine(folderChosen):
        if folderChosen != None:
            it = QDirIterator(folderChosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                        tela.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                    tela.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
            if(tela.playlist.mediaCount() > 0):
                tela.model.layoutChanged.emit()
                tela.player.play()
                tela.player.setPlaylist(tela.playlist)
                tela.player.playlist().setCurrentIndex(0)
                tela.lblMsgPlayer.setText("Arquivos carregados");
            else:
                tela.lblMsgPlayer.setText("Nenhum arquivo encontrado");        
        else:
            tela.lblMsgPlayer.setText("Processo de carregamento cancelado!");


    def erroralert(self, *args):
        print(args)
    
    def playhandler():
        if tela.playlist.mediaCount() == 0:
            tela.lblMsgPlayer.setText("Nenhum arquivo carregado!")
        elif tela.playlist.mediaCount() != 0:
            if(tela.userAction == 1):
                icon = QIcon()
                icon.addPixmap(QPixmap("Icones/Play2.png"), QIcon.Normal, QIcon.Off)
                tela.btnPlay.setIcon(icon)
                tela.player.pause()
                tela.userAction = 2
            else:
                icon = QIcon()
                icon.addPixmap(QPixmap("Icones/pause2.png"), QIcon.Normal, QIcon.Off)
                tela.btnPlay.setIcon(icon)
                tela.player.play()
                tela.userAction = 1
                            
    def songChanged(media):
        if not media.isNull():
            url = media.canonicalUrl()
            tela.statusbar.showMessage("Tocando - " + url.fileName())

    def prevSong():
        if tela.playlist.mediaCount() == 0:
            tela.lblMsgPlayer.setText("Nenhum arquivo carregado!");
        elif tela.playlist.mediaCount() != 0:
            tela.player.playlist().previous()
            icon = QIcon()
            icon.addPixmap(QPixmap("Icones/Play2.png"), QIcon.Normal, QIcon.Off)
            tela.btnPlay.setIcon(icon)  
            

    def nextSong():
        if tela.playlist.mediaCount() == 0:
            tela.lblMsgPlayer.setText("Nenhum arquivo carregado!");
        elif tela.playlist.mediaCount() != 0:
            tela.player.playlist().next()


    def stophandler():
        icon = QIcon()
        icon.addPixmap(QPixmap("Icones/Play2.png"), QIcon.Normal, QIcon.Off)
        tela.btnPlay.setIcon(icon)        
        tela.userAction = 0
        tela.player.stop()


    def updateDuration(duration):
        tela.sldMusicPos.setMaximum(duration)
        if duration >= 0:
            tela.lblTempoTotal.setText(Player.convertTempo(duration))

    def updatePosition(position):
        if position >= 0:
            tela.lblTempoMusica.setText(Player.convertTempo(position))
        tela.sldMusicPos.blockSignals(True)
        tela.sldMusicPos.setValue(position)
        tela.sldMusicPos.blockSignals(False)

    def playlistPositionChanged(i):
        if i > -1:
            ix = tela.model.index(i)
            tela.listMusic.setCurrentIndex(ix)

    def playlistSelectionChanged(ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        tela.playlist.setCurrentIndex(i)

    #Final do Player de musica