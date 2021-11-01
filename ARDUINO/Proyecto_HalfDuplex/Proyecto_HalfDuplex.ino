int sensor1 = A0;
int sensor2 = A1;
int sensor3 = A2;

int ledaccion3 = 13;
int ledaccion2 = 12;
int ledaccion1 = 11;

int valor1;
int valor2;
int valor3;

float nums[3];
byte arr[3];

void setup() {
  pinMode(ledaccion1,OUTPUT);
  pinMode(ledaccion2,OUTPUT);
  pinMode(ledaccion3,OUTPUT);
  
  Serial.begin(9600);
  Serial.setTimeout(100);
}

String accion;
char *s; //apuntador->arreglo declarado y recepcion

void loop() { 
     if(Serial.available()>0){   //arduino verifica si se le envio informacion 
        accion= Serial.readString(); // va a transformar a string lo que se le recibio  "0.11,0.12,0.13"       
        s=strtok(accion.c_str(),","); // separa los caracteres usando la coma como punto de referencia y te devuelve el primero
                                      //por ejemplo 0.11

        for(int i=0; i<3&&s!=NULL;i++){
           nums[i]= String(s).toFloat(); //transformar el arreglo de chars a string y luego flotante
           s = strtok(NULL, ",");} //es para deveolver los siguientes numeros, por ejemplo en la perimera iteracion te devolvera el 0,12
                                     //luego en otra vuelta el 0.13
       PrenderApagar();}
  
    valor1 = analogRead(sensor1);
    valor2 = analogRead(sensor2);
    valor3 = analogRead(sensor3);
    
    Serial.println("I" +String(valor1) +"R"
    + String(valor2) +"R"+ String(valor3) + "F");
  
  delay (100);}

void PrenderApagar(){
  
  //te busca cual es el mayor
  float mayor= nums[0];
  int i;  
    for(i=1; i<3; i++){
      if(nums[i]>mayor){
        mayor=nums[i]; 
      }}

  int rep=0;
    for(i=0; i<3; i++){
      //verifica si el numero actual, es igual al mayor
      if(nums[i]==mayor){
        arr[i]=1; 
        //si es igual lo guardo en un arreglo un 1 para indicarle a futuro que voy a prender el led
        rep++;
      }else{
        arr[i]=0;
        //en caso contrario le pongo cero para indicarle que lo voy a apagar
      }}
  
    if(rep==3){
      //si de pura casualidad rep vale  3  indicara que todos los numeros son iguales
      //y por ende ninguno es el mayor
      arr[0]=arr[1]=arr[2]=0;}
        
    digitalWrite(ledaccion1, arr[0]);
    digitalWrite(ledaccion2, arr[1]);
    digitalWrite(ledaccion3, arr[2]); 
 }
