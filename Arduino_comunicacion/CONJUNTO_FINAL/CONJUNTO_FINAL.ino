// Variables para los pines
const int ledPin = 13;  // Pin del LED integrado
const int pwmPin = 9;   // Pin para control de PWM
int pwmValue = 0;       // Valor para el control de intensidad PWM

void setup() {
  // Inicializamos la comunicación serial
  Serial.begin(9600);

  // Configuramos el pin del LED como salida
  pinMode(ledPin, OUTPUT);

  // Configuramos el pin de PWM como salida
  pinMode(pwmPin, OUTPUT);
}

void loop() {
  // Verificamos si hay datos disponibles en la comunicación serial
  if (Serial.available() > 0) {
    // Leemos el comando que envía el programa en Python
    String command = Serial.readStringUntil('\n');
    command.trim();  // Eliminamos cualquier espacio o salto de línea adicional

    // Comandos para encender/apagar el LED
    if (command == "1") {
      digitalWrite(ledPin, HIGH);  // Enciende el LED
      Serial.println("LED encendido");
    }
    else if (command == "0") {
      digitalWrite(ledPin, LOW);   // Apaga el LED
      Serial.println("LED apagado");
    }

    // Comando para realizar una suma (comienza con 'S')
    else if (command.startsWith("S")) {
      int number = command.substring(1).toInt();  // Extraemos el número después de la 'S'
      int result = number + 1;  // Realizamos la suma
      Serial.println(result);  // Devolvemos el resultado al programa en Python
    }

    // Comando para ajustar la intensidad PWM (comienza con 'P')
    else if (command.startsWith("P")) {
      int pwm = command.substring(1).toInt();  // Extraemos el número después de la 'P'
      if (pwm >= 0 && pwm <= 255) {
        analogWrite(pwmPin, pwm);  // Ajustamos la intensidad PWM
        Serial.println("Intensidad PWM ajustada");
      } else {
        Serial.println("Valor PWM fuera de rango");
      }
    }

    // Comando para leer un valor 
    else if (command == "LEER") {
      float sensorValue = analogRead(A0);  // Leemos un valor del pin A0
      float vol = (sensorValue*5.0)/1023.0;
      Serial.println(vol);  // Devolvemos el valor al programa en Python
    }
  }
}
