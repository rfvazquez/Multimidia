#import RPi.GPIO as GPIO

class ControleCarro():
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
        self.lblImagem.setPixmap(QPixmap("Icones/"+imagem+".png"))
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
        
    def testeControleCarro():
        print("teste")


    #Fim controle veiculo