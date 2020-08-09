import serial

class DataReceiver(): 
    #Configurações da Porta Serial
    def __init__(self):
        self.arduino = serial.Serial()
        self.arduino.port = "COM2"

        #Tempo de aguardo por uma resposta do arduino em segundos antes de encerrar conexao
        #Tem que ser maior entre o delay de envio de informacoes do sensores
        self.arduino.timeout = 20

        #Dict de medicoes
        self.medicoes = {}

    def close(self):
        self.arduino.close()
    
    def open(self):
        self.arduino.open()

    def build_dict(self, sensor_name): 
        sensor = {}
        sensor["namePlant"] = sensor_name
        sensor["temperatureAir"] = "Inativo"
        sensor["humidityAir"] = "Inativo"
        sensor["humiditySoil"] = "Inativo"
        return sensor

    def format_data(self, string_serial):
        string_parser = string_serial.split(':')
        sensor_name = string_parser[0]
        sensor_values = string_parser[1]
        sensor_values = sensor_values.split(',')

        sensor = self.build_dict(sensor_name)

        for value in sensor_values:
            value_parser = value.split('=')
            if value_parser[0] == "temperatureAir":
                if float(value_parser[1]) > 0:
                    sensor["temperatureAir"] = "Ativo"
            if value_parser[0] == "humidityAir":
                if float(value_parser[1]) > 20:
                    sensor["humidityAir"] = "Ativo"
            if value_parser[0] == "humiditySoil":
                if float(value_parser[1]) > 0:
                    sensor["humiditySoil"] = "Ativo"

        self.medicoes[sensor_name] = sensor

    def receive_data(self):
        string_serial = str(self.arduino.readline())
        string_serial = string_serial.replace("b'", "")
        string_serial = string_serial[:-5]
        self.format_data(string_serial)

        return string_serial
    

def main():
    data_receiver = DataReceiver() 
    data_receiver.close()
    data_receiver.open()
    while True:
        data_receiver.receive_data()
        print(data_receiver.medicoes)

main()
