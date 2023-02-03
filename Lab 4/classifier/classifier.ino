/****************************************************************
 * Example1_Basics.ino
 * Original script: ICM 20948 Arduino Library Demo
 * Use the default configuration to stream 9-axis IMU data
 * Owen Lyke @ SparkFun Electronics
 * Original Creation Date: April 17 2019
 *
 * Please see License.md for the license information.
 *
 * Distributed as-is; no warranty is given.
 * Modified to classify by Anna Anderson & Katherine Stahnke
 ***************************************************************/
#include "ICM_20948.h" // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU
//#define USE_SPI       // Uncomment this to use SPI
#define SERIAL_PORT Serial
#define SPI_PORT SPI // Your desired SPI port.       Used only when "USE_SPI" is defined
#define CS_PIN 2     // Which pin you connect CS to. Used only when "USE_SPI" is defined
#define WIRE_PORT Wire // Your desired Wire port.      Used when "USE_SPI" is not defined
#define AD0_VAL 1

#ifdef USE_SPI
ICM_20948_SPI myICM; // If using SPI create an ICM_20948_SPI object
#else
ICM_20948_I2C myICM; // Otherwise create an ICM_20948_I2C object
#endif

//LED values for calibration
#define LED_GREEN 4
#define LED_BLUE 12
#define LED_RED 15

//Accelerometer threshold vals for idle motion
float max_x = 0;
float max_y = 0;
float max_z = 0;
float min_x = 0;
float min_y = 0;
float min_z = 0;

void setup()
{
  pinMode(LED_BLUE, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  SERIAL_PORT.begin(115200);
  while (!SERIAL_PORT)
  {
  };

#ifdef USE_SPI
  SPI_PORT.begin();
#else
  WIRE_PORT.begin();
  WIRE_PORT.setClock(400000);
#endif
  //myICM.enableDebugging(); // Uncomment this line to enable helpful debug messages on Serial
  bool initialized = false;
  while (!initialized)
  {
#ifdef USE_SPI
    myICM.begin(CS_PIN, SPI_PORT);
#else
    myICM.begin(WIRE_PORT, AD0_VAL);
#endif
    SERIAL_PORT.print(F("Initialization of the sensor returned: "));
    SERIAL_PORT.println(myICM.statusString());
    if (myICM.status != ICM_20948_Stat_Ok)
    {
      SERIAL_PORT.println("Trying again...");
      delay(500);
    }
    else
    {
      initialized = true;
    }
  }
}
//End setup

bool calibrated = 0;
bool idle = 1;

float temp_x;
float temp_y;
float temp_z;

float gyr_x;
float gyr_y;
float gyr_z;

void loop()
{
  
  if (myICM.dataReady())
  {
    myICM.getAGMT(); // The values are only updated when you call 'getAGMT'
    if (!calibrated) {
       SERIAL_PORT.println("Calibrating idle movement"); 
       digitalWrite(LED_BLUE, HIGH);
       for (int i = 0; i < 10; i++)
        {
          delay(1000);
          // Get Max & Min Acceleration
          if (myICM.accX()> max_x) {
            max_x = myICM.accX();
          }
          if (myICM.accY()> max_y) {
            max_y = myICM.accY();
          }
          if (myICM.accZ()> max_z) {
            max_z = myICM.accZ();
          }
          //Get min
          if (myICM.accX()< min_x) {
            min_x = myICM.accX();
          }
          if (myICM.accY()< min_y) {
            min_y = myICM.accY();
          }
          if (myICM.accZ()< min_z) {
            min_z = myICM.accZ();
          }
        }
        SERIAL_PORT.println("Idle values:");
        SERIAL_PORT.println( min_x);
        SERIAL_PORT.println( max_x);
        SERIAL_PORT.println( min_y);
        SERIAL_PORT.println( max_y);
        SERIAL_PORT.println( min_z);
        SERIAL_PORT.println(max_z); 
        digitalWrite(LED_BLUE, LOW);
        calibrated = 1; //Set calibration mode to true
    }

    //SERIAL_PORT.println("OUT OF CALIBARTION");
    
    temp_y = myICM.accY();
    temp_z = myICM.accZ();
    temp_x = myICM.accX();
    
    gyr_y = myICM.gyrY();
    gyr_z = myICM.gyrZ();
    gyr_x = myICM.gyrX();
    
    delay(50);
    myICM.getAGMT();
    float diff_x = myICM.accX() - temp_x;
    float diff_y = myICM.accY() - temp_y;
    float diff_z = myICM.accZ() - temp_z;

    float dgyr_x = myICM.gyrX() - gyr_x;
    float dgyr_y = myICM.gyrY() - gyr_y;
    float dgyr_z = myICM.gyrZ() - gyr_z;

    //Detect forward movement
    if (myICM.accZ() < max_z + 100 && myICM.accZ() > min_z - 100
    && myICM.accX() < max_x + 100 && myICM.accX() > min_x - 100
    && myICM.accY() < max_y + 100 && myICM.accY() > min_y - 100) {
      SERIAL_PORT.println("IDLE!");
    }
    else if (abs(diff_x) > 800 && abs(diff_y) < 500 && abs(diff_z) < 500) {
      SERIAL_PORT.println("FORWARD MOVEMENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
    }
    else if (abs(diff_z) > 800 && abs(diff_y) < 500 && abs(diff_x) < 500) {
      SERIAL_PORT.println("UPWARD MOVEMENT********************************");
    }
    else if (abs(dgyr_x) > 100 && abs(dgyr_y) < 50 && abs(dgyr_z) < 50) {
      SERIAL_PORT.println("CIRCULAR MOVEMENTs---------------------------------------");
    }
    //printScaledAGMT(&myICM); // This function takes into account the scale settings from when the measurement was made to calculate the values with units
    //delay(30);
  }
  else
  {
    SERIAL_PORT.println("Waiting for data");
    delay(500);
  }
}

// Below here are some helper functions to print the data nicely!

void printPaddedInt16b(int16_t val)
{
  if (val > 0)
  {
    SERIAL_PORT.print(" ");
    if (val < 10000)
    {
      SERIAL_PORT.print("0");
    }
    if (val < 1000)
    {
      SERIAL_PORT.print("0");
    }
    if (val < 100)
    {
      SERIAL_PORT.print("0");
    }
    if (val < 10)
    {
      SERIAL_PORT.print("0");
    }
  }
  else
  {
    SERIAL_PORT.print("-");
    if (abs(val) < 10000)
    {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 1000)
    {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 100)
    {
      SERIAL_PORT.print("0");
    }
    if (abs(val) < 10)
    {
      SERIAL_PORT.print("0");
    }
  }
  SERIAL_PORT.print(abs(val));
}

void printRawAGMT(ICM_20948_AGMT_t agmt)
{
  SERIAL_PORT.print("RAW. Acc [ ");
  printPaddedInt16b(agmt.acc.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.acc.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.acc.axes.z);
  SERIAL_PORT.print(" ], Gyr [ ");
  printPaddedInt16b(agmt.gyr.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.gyr.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.gyr.axes.z);
  SERIAL_PORT.print(" ], Mag [ ");
  printPaddedInt16b(agmt.mag.axes.x);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.mag.axes.y);
  SERIAL_PORT.print(", ");
  printPaddedInt16b(agmt.mag.axes.z);
  SERIAL_PORT.print(" ], Tmp [ ");
  printPaddedInt16b(agmt.tmp.val);
  SERIAL_PORT.print(" ]");
  SERIAL_PORT.println();
}

void printFormattedFloat(float val, uint8_t leading, uint8_t decimals)
{
  float aval = abs(val);
  if (val < 0)
  {
    SERIAL_PORT.print("-");
  }
  else
  {
    SERIAL_PORT.print(" ");
  }
  for (uint8_t indi = 0; indi < leading; indi++)
  {
    uint32_t tenpow = 0;
    if (indi < (leading - 1))
    {
      tenpow = 1;
    }
    for (uint8_t c = 0; c < (leading - 1 - indi); c++)
    {
      tenpow *= 10;
    }
    if (aval < tenpow)
    {
      SERIAL_PORT.print("0");
    }
    else
    {
      break;
    }
  }
  if (val < 0)
  {
    SERIAL_PORT.print(-val, decimals);
  }
  else
  {
    SERIAL_PORT.print(val, decimals);
  }
}

#ifdef USE_SPI
void printScaledAGMT(ICM_20948_SPI *sensor)
{
#else
void printScaledAGMT(ICM_20948_I2C *sensor)
{
#endif
  SERIAL_PORT.print("Scaled. Acc (mg) [ ");
  printFormattedFloat(sensor->accX(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->accY(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->accZ(), 5, 2);
  SERIAL_PORT.print(" ], Gyr (DPS) [ ");
  printFormattedFloat(sensor->gyrX(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->gyrY(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->gyrZ(), 5, 2);
  SERIAL_PORT.print(" ], Mag (uT) [ ");
  printFormattedFloat(sensor->magX(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->magY(), 5, 2);
  SERIAL_PORT.print(", ");
  printFormattedFloat(sensor->magZ(), 5, 2);
  SERIAL_PORT.print(" ], Tmp (C) [ ");
  printFormattedFloat(sensor->temp(), 5, 2);
  SERIAL_PORT.print(" ]");
  SERIAL_PORT.println();
}
