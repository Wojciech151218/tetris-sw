 #include <Adafruit_NeoPixel.h>


#define PIN 6
#define WIDTH 8
#define HEIGHT 32
#define NUM_PIXELS (WIDTH * HEIGHT)

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

void displayPixel(Pixel pixel) {
    if (pixel.x < 0 || pixel.x >= WIDTH) return;
    if (pixel.y < 0 || pixel.y >= HEIGHT) return;

    int index = xyToIndex(pixel.x, pixel.y);

    uint32_t rgb = colorToRGB(pixel.color);

    strip.setPixelColor(index, rgb);
}

void displayCsv(char *csv) {
    int pos = 0;

    while (csv[pos] != '\0') {
      

        // Parse X
        int x = 0;
        while (csv[pos] >= '0' && csv[pos] <= '9') {
            x = x * 10 + (csv[pos] - '0');
            pos++;
        }
        if (csv[pos] != ';') return;
        pos++;

        // Parse Y
        int y = 0;
        while (csv[pos] >= '0' && csv[pos] <= '9') {
            y = y * 10 + (csv[pos] - '0');
            pos++;
        }
        if (csv[pos] != ';') return;
        pos++;

        // Parse color char
        char c = csv[pos];
        pos++;

        // Skip to next line
        while (csv[pos] == '\r' || csv[pos] == '\n') pos++;

        Pixel pixel = {
            (short)x,
            (short)y,
            c
        };
        if(x>= WIDTH || x < 0 || y>= HEIGHT || y <0){
          Serial.println("recieved pixel doesnt fit on the screen");
          return;
        }
        displayPixel(pixel);
    }
}

bool readCsvFromUart(char *buffer, int bufferSize) {
    static int bufferIndex = 0;
    
    // Read available data from Serial
    while (Serial.available() > 0) {
        char c = Serial.read();
        
        // Check for end of transmission (newline or null terminator)
        if (c == '\n' || c == '\r' || bufferIndex >= bufferSize - 1) {
            if (bufferIndex > 0) {
                buffer[bufferIndex] = '\0';  // Null terminate the string
                bufferIndex = 0;  // Reset buffer for next transmission
                return true;  // Complete CSV line received
            }
        } else {
            buffer[bufferIndex++] = c;  // Add character to buffer
        }
    }
    
    return false;  // No complete CSV line received yet
}

void setup() {
  Serial.begin(9600);   // or 115200
  Serial.println("Serial started!");
  strip.begin();

}

void loop() {
  static char csvBuffer[1792]; 

  if (readCsvFromUart(csvBuffer, sizeof(csvBuffer))) {
    strip.clear();    
    displayCsv(csvBuffer);
    strip.show();
  }
}
