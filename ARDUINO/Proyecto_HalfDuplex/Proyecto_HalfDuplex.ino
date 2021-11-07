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
char *s; 

void loop() { 
     if(Serial.available()>0){  
        accion= Serial.readString();      
        s=strtok(accion.c_str(),",");

        for(int i=0; i<3&&s!=NULL;i++){
           nums[i]= String(s).toFloat(); 
           s = strtok(NULL, ",");} 
       PrenderApagar();}
  
    valor1 = analogRead(sensor1);
    valor2 = analogRead(sensor2);
    valor3 = analogRead(sensor3);
    
    Serial.println("I" +String(valor1) +"R"
    + String(valor2) +"R"+ String(valor3) + "F");
  
  delay (100);}

void PrenderApagar(){
  float mayor= nums[0];
  int i;  
    for(i=1; i<3; i++){
      if(nums[i]>mayor){
        mayor=nums[i]; 
      }}

  int rep=0;
    for(i=0; i<3; i++){
      if(nums[i]==mayor){
        arr[i]=1; 
        rep++;
      }else{
        arr[i]=0;
      }}
  
    if(rep==3){
      arr[0]=arr[1]=arr[2]=0;}
        
    digitalWrite(ledaccion1, arr[0]);
    digitalWrite(ledaccion2, arr[1]);
    digitalWrite(ledaccion3, arr[2]); 
 }
