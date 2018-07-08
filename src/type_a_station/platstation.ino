#include "DHT.h"
#include "mcp_can.h"
#include <SPI.h>
#include "siren.h"

#define PIN_SOIL_MOISTURE  5    
#define PIN_SPRINKLER0 3    
#define DHTPIN A0 // A0

int val;
int sprinkler_state = LOW;


#define CONTROL_CYCLE 500
#define RECEIVE_CYCLE 10



unsigned long last_time_control_triggered;
unsigned long last_time_recv_triggered;


DHT dht(DHTPIN, DHT11);
MCP_CAN CAN0(10);     // Set CS to pin 10

struct SirenSprinklerStatus_t sprinkler_status;

struct SirenDispatcher_t dispatcher;

  
   void on_Sprinkle_Command(struct SirenDispatcher_t* d, uint32_t arb_id, struct SirenSprinkle_Command_t *msg){
    Serial.println("sprinkle command received");
    sprinkler_status.Sprinkler1 = msg->Sprinkler1;
    sprinkler_status.Sprinkler2 = msg->Sprinkler2;
    sprinkler_status.Sprinkler3 = msg->Sprinkler3;
    sprinkler_status.Sprinkler4 = msg->Sprinkler4;
    
   }
   
   void on_Ping(struct SirenDispatcher_t* d, uint32_t arb_id, struct SirenPing_t *msg){
    Serial.println("ping");
   }

unsigned long time_passed(unsigned long  new_time, unsigned long  old_time){
  return old_time > new_time ? 1 + old_time + ~new_time : new_time - old_time;
}


void receive_can_data(){
        uint32_t id;
        uint8_t len;
        uint8_t message[8];
        
        uint8_t status = CAN0.readMsgBuf(&id, &len, message);
        if (status == CAN_OK)
        {
          Serial.println(status);
          Serial.println(message[0]);
          Siren_dispatch(&dispatcher, id, message);
        }
}

void receive_cycle(){
  unsigned long currentMillis = millis();
  unsigned long dt = time_passed(currentMillis, last_time_recv_triggered);
  if (dt >= RECEIVE_CYCLE){
    receive_can_data();
    last_time_recv_triggered = currentMillis;
  }
}






void send_can_data(){

    uint32_t id;
  uint8_t len;
  uint8_t message[8];
  struct SirenArbId arb_id;
  
   SirenSprinklerStatus_init(&arb_id, &sprinkler_status);

   SirenSprinklerStatus_encode(&sprinkler_status, message);
   id = SirenArbId_encode(&arb_id);

  byte sndStat = CAN0.sendMsgBuf(id, 1, 8, message);
  if(sndStat == CAN_OK){
    Serial.println("Message Sent Successfully!");
  } else {

    if (CAN0.getError() & MCP_EFLG_TXBO){
      Serial.println("Bus off");
    }
    else{
      Serial.println("Not Bus off");
      Serial.println(CAN0.getError());
    }
    
    Serial.println(sndStat);
  }


  
  
}

uint8_t to_pin_level(uint8_t logic){
  if (logic){
    return LOW;
  }else{
    return HIGH;
  }
}


void do_control(){
        val = analogRead(PIN_SOIL_MOISTURE);

        digitalWrite(PIN_SPRINKLER0+0, to_pin_level(sprinkler_status.Sprinkler1));
        digitalWrite(PIN_SPRINKLER0+1, to_pin_level(sprinkler_status.Sprinkler2));
        digitalWrite(PIN_SPRINKLER0+2, to_pin_level(sprinkler_status.Sprinkler3));
        digitalWrite(PIN_SPRINKLER0+3, to_pin_level(sprinkler_status.Sprinkler4));
      
        float rh = dht.readHumidity();
        float t = dht.readTemperature();
              
          Serial.print(rh); Serial.print(" %\t\t");
          Serial.print(t); Serial.print(" *C\t");      
}


void control_cycle(){
  unsigned long currentMillis = millis();
  unsigned long dt = time_passed(currentMillis, last_time_control_triggered);

  if (dt >= CONTROL_CYCLE){
        do_control();
         send_can_data();
        last_time_control_triggered = currentMillis;
  }
}


void setup() {
  unsigned long last_time_control_triggered = millis();
  unsigned long last_time_recv_triggered = millis();
  

  Serial.begin(9600);


  sprinkler_status.Sprinkler1 = 0;
  sprinkler_status.Sprinkler2 = 1;
  sprinkler_status.Sprinkler3 = 0;
  sprinkler_status.Sprinkler4 = 1;
  
  //Siren_init(&dispatcher);
  dispatcher.on_Sprinkle_Command_ptr = &on_Sprinkle_Command;
  dispatcher.on_Ping_ptr = &on_Ping;
  
  
  //pinMode(PIN_SPRINKLER, OUTPUT);
  for (int i=0; i<6; i++){
    pinMode(i+3, OUTPUT);  
  }
  
  dht.begin();   

  do_control();
  

  
  if(CAN0.begin(MCP_ANY, CAN_125KBPS, MCP_8MHZ) == CAN_OK) Serial.println("MCP2515 Initialized Successfully!");
  else Serial.println("Error Initializing MCP2515...");

  CAN0.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted


}

void loop(){
  receive_cycle();
  control_cycle();
  delay(10);
}


