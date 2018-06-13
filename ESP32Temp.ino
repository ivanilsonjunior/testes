#include <WiFi.h>
#include <DHTesp.h>
#include <WiFiUdp.h>
#include <time.h>

#include <EasyNTPClient.h>

const char* ssid = "wIFRN-IoT";
const char* password = "Ifrn@IoT!N0CFrZ";

WiFiServer server(80);
WiFiUDP udp;


#define DHTPIN 4
//#define DHTTYPE DHT11

DHTesp dht;//.setup(4, DHTesp::DHT11);

float temp = -1;
float humi = 0;
float hist[10] = {0,0,0,0,0,0,0,0,0,0};
float tempo[10] = {0,0,0,0,0,0,0,0,0,0};

int acesso = 0;
const int TEMPERATURE_INTERVAL = 10;
unsigned long last_temperature_sent = 0;

const int HUMIDITY_INTERVAL = 10;
unsigned long last_humidity_sent = 0;


void setup() {

  dht.setup(DHTPIN, DHTesp::DHT11);
  Serial.begin(115200);
  pinMode(5, OUTPUT);      // set the LED pin mode
  pinMode(4,  INPUT);

  
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }


    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
    server.begin();

}

void medir(){
   temp = dht.getTemperature();
   humi = dht.getHumidity();
   //tempo = {0,0,0,0,0,0,0,0,0,0};
   if (acesso > 10) {
      for (int i = 0 ; i < 9 ; i++) {
        tempo[i] = hist[i+1];
      }
      tempo[9] = temp;
      for (int i = 0 ; i < 10 ; i++) {
        hist[i] = tempo[i];
      }
      acesso++;
   } else {
      hist[acesso++] = temp;
   }
}

void loop() {
   WiFiClient client = server.available();   // listen for incoming clients
  
  if (client) {
    EasyNTPClient ntpClient(udp, "pool.ntp.org", (-(3*60*60))); // IST = GMT + 5:30
    medir();
    int unixTime = ntpClient.getUnixTime();
    //String hora = "" + // + ":" + getMinutes(unixTime) + ":" + getSeconds(unixTime);
    Serial.print(getHours(unixTime));Serial.print(":");Serial.print(getMinutes(unixTime));Serial.print(getSeconds(unixTime));
    Serial.println(unixTime);
    Serial.print("Temp: ");
    Serial.print(temp);
    Serial.print(" Humi: ");
    Serial.println(humi);// if you get a client,
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        if (c == '\n') {                    // if the byte is a newline character

          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:
            client.print("<html><head></head><body><Click <a href=\"/H\">here</a> to turn the LED on pin 5 on.<br>");
            client.print("Click <a href=\"/L\">here</a> to turn the LED on pin 5 off.<br>");
            client.print("<svg width=\"250\" height=\"150\"><polyline points=\"");

            int inicial = 15;
            int i;
            for (i = 0; i < 10; i++){
              client.print(inicial);
              client.print(",");
              client.print(100-(int(hist[i])*2));
              client.print(" ");
              inicial = inicial + 20;
            }
            int local = 0;
            if (acesso < 10) {
              local = acesso;
            } else {
              local = 9;
              }
            client.print("\" style=\"stroke:#006600; fill: none;\"/>");
            client.print("<circle cx=\"");
            client.print(15+(20*local));
            client.print("\" cy=\"");
            client.print(100-(int(hist[local])*2));
            client.print("\" r=\"3\" stroke=\"black\" stroke-width=\"1\" fill=\"none\" />");
            client.print("<text x=\"10\" y=\"20\" fill=\"red\">Temperatura ");
            client.print(temp);
            client.print("</text><polyline points=\"5,5  5,145  245,145  245,5 5,5\" style=\"stroke:#000000; fill: none\"/>\
    <line x1=\"5\" y1=\"100\" x2=\"245\" y2=\"100\" style=\"stroke: #000000 ;stroke-width:2\" />\
    <line stroke-dasharray=\"2,2\" x1=\"5\" y1=\"80\" x2=\"245\" y2=\"80\" style=\"stroke: #000000 ;stroke-width:1\" />\
    <line stroke-dasharray=\"2,2\" x1=\"5\" y1=\"60\" x2=\"245\" y2=\"60\" style=\"stroke: #000000 ;stroke-width:1\" />\
    <line stroke-dasharray=\"2,2\" x1=\"5\" y1=\"40\" x2=\"245\" y2=\"40\" style=\"stroke: #000000 ;stroke-width:1\" />\
    <line stroke-dasharray=\"2,2\" x1=\"5\" y1=\"20\" x2=\"245\" y2=\"20\" style=\"stroke: #000000 ;stroke-width:1\" />\
    <text x=\"220\" y=\"100\" fill=\"red\">0</text>\
    <text x=\"220\" y=\"80\" fill=\"red\">10</text>\
    <text x=\"220\" y=\"60\" fill=\"red\">20</text>\
    <text x=\"220\" y=\"40\" fill=\"red\">30</text>\
    <text x=\"220\" y=\"20\" fill=\"red\">40</text></svg></body></html>");


            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {    // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        // Check to see if the client request was "GET /H" or "GET /L":
        if (currentLine.endsWith("GET /H")) {
          digitalWrite(5, HIGH);               // GET /H turns the LED on
        }
        if (currentLine.endsWith("GET /L")) {
          digitalWrite(5, LOW);                // GET /L turns the LED off
        }
      }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
}

inline int getSeconds(uint32_t UNIXTime) {
  return UNIXTime % 60;
}

inline int getMinutes(uint32_t UNIXTime) {
  return UNIXTime / 60 % 60;
}

inline int getHours(uint32_t UNIXTime) {
  return UNIXTime / 3600 % 24;
}
