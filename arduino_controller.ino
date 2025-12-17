 #include <Adafruit_NeoPixel.h>


#define PIN 6
#define WIDTH 8
#define HEIGHT 32
#define NUM_PIXELS (WIDTH * HEIGHT)

#define MAX_CSV_LINE_SIZE 6

Adafruit_NeoPixel strip(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

struct Pixel {
    short x;
    short y;
    char color;
};

uint32_t colorToRGB(char c) {
    switch (c) {
        case 'r': return strip.Color(255, 0, 0);
        case 'g': return strip.Color(0, 255, 0);
        case 'b': return strip.Color(0, 0, 255);
        case 'y': return strip.Color(255, 255, 0);
        case 'p': return strip.Color(128, 0, 128);
        case 'o': return strip.Color(255, 70, 0);
        case 'w': return strip.Color(255, 255, 255);
        default:  return strip.Color(0, 0, 0);
    }
}
int xyToIndex(int x, int y) {
    if (y % 2 == 0) {
        // even row → normal
        return y * WIDTH + x;
    } else {
        // odd row → reversed
        return y * WIDTH + (WIDTH - 1 - x);
    }
}

void displayPixel(const Pixel & pixel) {
    if (pixel.x < 0 || pixel.x >= WIDTH) return;
    if (pixel.y < 0 || pixel.y >= HEIGHT) return;

    int index = xyToIndex(pixel.x, pixel.y);

    uint32_t rgb = colorToRGB(pixel.color);

    strip.setPixelColor(index, rgb);
}
void logPixel(const Pixel & pixel){
  Serial.print("x : ");
  Serial.print(pixel.x);
  Serial.print(" y : ");
  Serial.print(pixel.y);
  Serial.print(" color : ");
  Serial.println(pixel.color); 
}

void displayCsvLine(const char *csv) {
    uint8_t pos = 0;

    // Parse X
    uint16_t x = 0;
    while (csv[pos] >= '0' && csv[pos] <= '9') {
        x = x * 10 + (csv[pos] - '0');
        pos++;
    }
    if (csv[pos] != ';') return;
    pos++;

    // Parse Y
    uint16_t y = 0;
    while (csv[pos] >= '0' && csv[pos] <= '9') {
        y = y * 10 + (csv[pos] - '0');
        pos++;
    }
    if (csv[pos] != ';') return;
    pos++;

    // Parse color
    if (csv[pos] == '\0') return;
    char c = csv[pos];

    // Bounds check BEFORE creating pixel
    if (x >= WIDTH || y >= HEIGHT) {
        Serial.println(F("received pixel doesnt fit on the screen"));
        return;
    }

    Pixel pixel = {
        (short)x,
        (short)y,
        c
    };
    Serial.println(csv);
    logPixel(pixel);

    displayPixel(pixel);
}

void displayCsvFromUart() {
    static uint16_t bufferIndex = 0;
    static char csvLineBuffer[MAX_CSV_LINE_SIZE + 1];

    while (Serial.available() > 0) {
        char c = Serial.read();

        // Ignore CR (Serial Monitor sends CRLF)
        if (c == '\r') {
            continue;
        }

        // End of entire message
        if (c == '\0') {
            if (bufferIndex > 0) {
                csvLineBuffer[bufferIndex] = '\0';
                displayCsvLine(csvLineBuffer);
                Serial.println("message received");
                bufferIndex = 0;
            }
            return;
        }

        // End of one CSV line
        if (c == '\n') {
            csvLineBuffer[bufferIndex] = '\0';
            displayCsvLine(csvLineBuffer);
            bufferIndex = 0;
            continue;
        }

        // Store character if space remains
        if (bufferIndex < MAX_CSV_LINE_SIZE) {
            csvLineBuffer[bufferIndex++] = c;
        }
        // else: silently discard extra chars to prevent overflow
    }

}


void setup() {
  Serial.begin(9600);   // or 115200
  Serial.println("Serial started!");
  strip.begin();
  strip.setBrightness(32);
  strip.clear();
}

bool test = false;
void loop() {
  // char * testCsvLine = test ? "0;0;b\n" : "0;1;r\n";
  // test = !test;
  // delay(100);

  strip.clear(); 
  displayCsvFromUart();
  //displayCsvLine(testCsvLine);
  strip.show();
  delay(300);
  
}
