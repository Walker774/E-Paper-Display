/**
 * Based on espprogram.ino
 * Author: Aiya Girio
 * Last Modified: Nov 23 2022
 * This program communicates with a control server via HTTP and displays data on a 2.9" waveshare E-paper display
 */
#include <Arduino.h>
//Wifi Libraries
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
//SPI display Libraries
#include <SPI.h>
#include <GxEPD2_BW.h> // including both doesn't use more code or ram
#include <GxEPD2_3C.h> // including both doesn't use more code or ram
#include <U8g2_for_Adafruit_GFX.h>
//Character/string libraries
#include <string.h>
#include <stdio.h>
#include <iostream>
//Define serial output
#define USE_SERIAL Serial
//setup wifi
WiFiMulti wifiMulti;
//SPI pin assignments
GxEPD2_BW<GxEPD2_290_T94_V2, GxEPD2_290_T94_V2::HEIGHT> display(GxEPD2_290_T94_V2(/*CS=5*/ SS, /*DC=*/ 17, /*RST=*/ 16, /*BUSY=*/ 4)); // GDEM029T94, Waveshare 2.9" V2 variant
//font assignment
U8G2_FOR_ADAFRUIT_GFX u8g2Fonts;

//Wifi Cert
/*
const char* ca = \ 
"-----BEGIN CERTIFICATE-----\n" \  
"MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/\n" \  
"MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT\n" \  
"DkRTVCBSb290IENBIFgzMB4XDTE2MDMxNzE2NDA0NloXDTIxMDMxNzE2NDA0Nlow\n" \  
"SjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUxldCdzIEVuY3J5cHQxIzAhBgNVBAMT\n" \  
"GkxldCdzIEVuY3J5cHQgQXV0aG9yaXR5IFgzMIIBIjANBgkqhkiG9w0BAQEFAAOC\n" \  
"AQ8AMIIBCgKCAQEAnNMM8FrlLke3cl03g7NoYzDq1zUmGSXhvb418XCSL7e4S0EF\n" \  
"q6meNQhY7LEqxGiHC6PjdeTm86dicbp5gWAf15Gan/PQeGdxyGkOlZHP/uaZ6WA8\n" \  
"SMx+yk13EiSdRxta67nsHjcAHJyse6cF6s5K671B5TaYucv9bTyWaN8jKkKQDIZ0\n" \  
"Z8h/pZq4UmEUEz9l6YKHy9v6Dlb2honzhT+Xhq+w3Brvaw2VFn3EK6BlspkENnWA\n" \  
"a6xK8xuQSXgvopZPKiAlKQTGdMDQMc2PMTiVFrqoM7hD8bEfwzB/onkxEz0tNvjj\n" \  
"/PIzark5McWvxI0NHWQWM6r6hCm21AvA2H3DkwIDAQABo4IBfTCCAXkwEgYDVR0T\n" \  
"AQH/BAgwBgEB/wIBADAOBgNVHQ8BAf8EBAMCAYYwfwYIKwYBBQUHAQEEczBxMDIG\n" \  
"CCsGAQUFBzABhiZodHRwOi8vaXNyZy50cnVzdGlkLm9jc3AuaWRlbnRydXN0LmNv\n" \  
"bTA7BggrBgEFBQcwAoYvaHR0cDovL2FwcHMuaWRlbnRydXN0LmNvbS9yb290cy9k\n" \  
"c3Ryb290Y2F4My5wN2MwHwYDVR0jBBgwFoAUxKexpHsscfrb4UuQdf/EFWCFiRAw\n" \  
"VAYDVR0gBE0wSzAIBgZngQwBAgEwPwYLKwYBBAGC3xMBAQEwMDAuBggrBgEFBQcC\n" \  
"ARYiaHR0cDovL2Nwcy5yb290LXgxLmxldHNlbmNyeXB0Lm9yZzA8BgNVHR8ENTAz\n" \  
"MDGgL6AthitodHRwOi8vY3JsLmlkZW50cnVzdC5jb20vRFNUUk9PVENBWDNDUkwu\n" \  
"Y3JsMB0GA1UdDgQWBBSoSmpjBH3duubRObemRWXv86jsoTANBgkqhkiG9w0BAQsF\n" \  
"AAOCAQEA3TPXEfNjWDjdGBX7CVW+dla5cEilaUcne8IkCJLxWh9KEik3JHRRHGJo\n" \  
"uM2VcGfl96S8TihRzZvoroed6ti6WqEBmtzw3Wodatg+VyOeph4EYpr/1wXKtx8/\n" \  
"wApIvJSwtmVi4MFU5aMqrSDE6ea73Mj2tcMyo5jMd6jmeWUHK8so/joWUoHOUgwu\n" \  
"X4Po1QYz+3dszkDqMp4fklxBwXRsW10KXzPMTZ+sOPAveyxindmjkW8lGy+QsRlG\n" \  
"PfZ+G6Z6h7mjem0Y+iWlkYcV4PIWL1iwBi8saCbGS5jN2p8M+X+Q7UNKEkROb3N6\n" \  
"KOqkqm57TH2H3eDJAkSnh6/DNFu0Qg==\n" \  
"-----END CERTIFICATE-----\n";
*/

//*********Global Variables******************


void setup() 
{
  //Serial Setup
  USE_SERIAL.begin(115200);
  USE_SERIAL.println();
  USE_SERIAL.println();
  USE_SERIAL.println();
  for(uint8_t t = 4; t > 0; t--) 
  {
    USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
    USE_SERIAL.flush();
    delay(1000);
  }
  //wifi setup
  wifiMulti.addAP("Your SSID", "Your PASSWORD");//connect to wifi change when wifi details finalized *************************
  //esp details
  char ID[] = "A001"; //default ID *******************************************************************************************
  String mac = WiFi.macAddress(); 
  //Print ESP details for debugging
  Serial.print("ESP ID(mac addr):: ");//Prints ESP details 
  Serial.println(mac);
  Serial.print("Nickname:: ");
  Serial.println(ID);
}

void loop() 
{
  //variable definitions
  String instructions = "";

  // wait for WiFi connection
  if((wifiMulti.run() == WL_CONNECTED)) 
  {
    HTTPClient http;
        
    String mac = WiFi.macAddress(); 
    String ID = "A001"; //Not sure why this is repeated need to fix
    String URL = ("http://192.168.0.187:5000/labels/" + ID + ".txt"); //Your server IP+port+default label directory is /labels ******************************

    USE_SERIAL.print("[HTTP] begin...\n");
    http.begin(URL); //HTTP
        
    // start connection and send HTTP header
    int httpCode = http.GET();

    // httpCode will be negative on error
    if(httpCode > 0) 
    {
      // HTTP header has been send and Server response header has been handled
      USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);

      //Display init
      //Display Setup
      display.init();
      display.setTextColor(GxEPD_BLACK);
      display.firstPage();
      display.setRotation(1);
      u8g2Fonts.begin(display); // connect u8g2 procedures to Adafruit GFX

      //Display colors
      uint16_t bg = GxEPD_WHITE;
      uint16_t fg = GxEPD_BLACK;
      u8g2Fonts.setForegroundColor(fg);
      u8g2Fonts.setBackgroundColor(bg);

      // file found at server
      if(httpCode == HTTP_CODE_OK) 
      {
        instructions = http.getString();
        USE_SERIAL.println(instructions);
        //No new display update HTTP resonse will be *        
        if(instructions[0] == '*')
        {
          Serial.println("No new instructions detected, sleeping");
        }
        //Change the config settings HTTP response will be %
        else if(instructions[0] == '%')
        {
          Serial.println("New configuration saved");
        }
        //Update the display will new data response will be that data
        else 
        {
          //Display image
          do
          {
            String input[5] =  {""};
            char seperator = '\n';
            int currIndex = 0, i = 0;  
            int startIndex = 0, endIndex = 0;  
            while (i <= instructions.length())  
            {  
              if (instructions[i] == seperator || i == instructions.length())  
              {  
                endIndex = i;  
                String subStr = "";  
                input[currIndex] = instructions.substring(startIndex);  
                currIndex += 1;  
                startIndex = endIndex + 1;  
                Serial.println("Line: "+input[currIndex]);
              }  
            i++;  
            }

            String pName = input[0];
            String pPrice = input[1];
            String pUPC = input[2];
            String pDates = (input[3]+input[4]);

            display.fillScreen(GxEPD_WHITE);
    
            u8g2Fonts.setFont(u8g2_font_fur30_tr);
            u8g2Fonts.setCursor(0, 35); 
            u8g2Fonts.print(pName);

            u8g2Fonts.setFont(u8g2_font_fur30_tr);
            u8g2Fonts.setCursor(0, 72); 
            u8g2Fonts.print(pPrice);

            u8g2Fonts.setFont(u8g2_font_fur17_tr);
            u8g2Fonts.setCursor(0, 103); 
            u8g2Fonts.print(pUPC);
    
            u8g2Fonts.setFont(u8g2_font_7x13B_tr);
            u8g2Fonts.setCursor(0, 125); 
            u8g2Fonts.print(pDates);
          } 
          while(display.nextPage());
        }
      }   
    } 
    else 
    {
      USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }
  delay(60000);
}

