#include <Adafruit_NeoPixel.h>


#define PIN 6
#define WIDTH 8
#define HEIGHT 32
#define NUM_PIXELS (WIDTH * HEIGHT)

Adafruit_NeoPixel strip(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

enum Color {
    Red, Green, Blue, Yellow, Purple, Orange, White
};

struct Pixel {
    short x;
    short y;
    Color color;
};

Color getColor(char c) {
    switch (c) {
        case 'r': return Red;
        case 'g': return Green;
        case 'b': return Blue;
        case 'y': return Yellow;
        case 'p': return Purple;
        case 'o': return Orange;
        case 'w': return White;
        default:  return Red;
    }
}

uint32_t colorToRGB(Color c) {
    switch (c) {
        case Red:    return strip.Color(255, 0, 0);
        case Green:  return strip.Color(0, 255, 0);
        case Blue:   return strip.Color(0, 0, 255);
        case Yellow: return strip.Color(255, 255, 0);
        case Purple: return strip.Color(128, 0, 128);
        case Orange: return strip.Color(255, 70, 0);
        case White:  return strip.Color(255, 255, 255);
        default:     return strip.Color(0, 0, 0);
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
            getColor(c)
        };
        if(x>= WIDTH || x < 0 || y>= HEIGHT || y <0){
          Serial.println("recieved pixel doesnt fit on the screen");
          return;
        }
        displayPixel(pixel);
    }
}

void setup() {
  Serial.begin(9600);   // or 115200
  Serial.println("Serial started!");
  strip.begin();

}

void loop() {
  char * csv = "0;6;b\n0;5;r\n0;4;g\n";
  while(true){
    displayCsv(csv);
    strip.show();
  }


}
