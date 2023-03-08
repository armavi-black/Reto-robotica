//Librerias de ROS
#include <ros.h>
#include <std_msgs/Float32.h>

//Se instancia el manejador del nodo y mensaje de entrada
ros::NodeHandle nh;
std_msgs::Float32 input_msg;

//Variables
const int PinPWM = 5;
const int PinIN1 = 4;
const int PinIN2 = 0;
double input;
int output;

//Callback y subscriber
void inputCallback(const std_msgs::Float32& input_msg){
  input = input_msg.data;
}
ros::Subscriber<std_msgs::Float32> sub("cmd_pwm", &inputCallback);

void setup() {
  //Se inicia el nodo y se suscribe al topico
  nh.initNode();
  nh.subscribe(sub);
  // configuramos los pines como salida
  pinMode(PinIN1, OUTPUT);
  pinMode(PinIN2, OUTPUT);
  pinMode(PinPWM, OUTPUT);
}

void loop() {
  //Función que controla el driver del motor
  output = MotorDriver(input, PinPWM, PinIN1, PinIN2);

  nh.spinOnce();
  delay(1000);
}

//Función que controla el driver del motor
/*
  Params
  input : valor entre -1 y 1
  PWM : pin que manda la señal PWM
  IN1 : pin que se conecta al IN1
  IN2 : pin que se conecta al IN2
*/
int MotorDriver(double input, int PWM, int IN1, int IN2)
{
  int output;
  //Se procesa el input para saber magnitud y sentido
  int direction = 0;
  if (input != 0.0)
    direction = input / abs(input);
  int magnitude = abs(input) * 100;
  
  //Serial.println(direction);
  //Serial.println(magnitude);

  //Se manda al driver la dirección de rotación
  if(direction < 0){
    digitalWrite (IN1, LOW);
    digitalWrite (IN2, HIGH);
    //Serial.println("Sentido antihorario");
  }
  else if(direction > 0){
    digitalWrite (IN1, HIGH);
    digitalWrite (IN2, LOW);
    //Serial.println("Sentido horario");
  }
  else{
    digitalWrite (IN1, LOW);
    digitalWrite (IN2, LOW);
    //Serial.println("Motor Detenido");
  }

  //Se manda la velocidad del motor con PWM
  int dutyCycle = map(magnitude,0,100,0,255);
  analogWrite(PWM, dutyCycle);
  //Serial.println(dutyCycle);
  output = direction*magnitude;
  //Serial.println("-----------------------------------");
  return output;
}
