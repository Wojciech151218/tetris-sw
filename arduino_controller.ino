#include <Adafruit_NeoPixel.h>

#define PIN 6
#define WIDTH 8
#define HEIGHT 32
#define NUM_PIXELS (WIDTH * HEIGHT)

#define MAX_CSV_LINE_SIZE 8   

Adafruit_NeoPixel strip(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

const bool LOG_ENABLED = true;

uint32_t colorToRGB(char c) {
    switch (c) {
        case 'r': return strip.Color(255, 0, 0);
        case 'g': return strip.Color(0, 255, 0);
        case 'b': return strip.Color(0, 0, 255);
        case 'y': return strip.Color(255, 255, 0);
        case 'p': return strip.Color(128, 0, 128);
        case 'o': return strip.Color(255, 70, 0);
        case 'w': return strip.Color(255, 255, 255);
        default:  return 0;
    }
}

int xyToIndex(int x, int y) {
    if (y & 1) {
        return (HEIGHT - 1 - y) * WIDTH + (WIDTH - 1 - x);
    } else {
        return (HEIGHT - 1 - y) * WIDTH + x;
    }
}

void displayCsvLine(const char *csv) {
    uint8_t pos = 0;
    uint8_t x = 0;
    uint8_t y = 0;

    while (csv[pos] >= '0' && csv[pos] <= '9') {
        x = x * 10 + (csv[pos++] - '0');
    }
    if (csv[pos++] != ';') {
        if (LOG_ENABLED) {
            Serial.print("CSV parse error: expected ';' after x: ");
            Serial.println(csv);
        }
        return;
    }

    while (csv[pos] >= '0' && csv[pos] <= '9') {
        y = y * 10 + (csv[pos++] - '0');
    }
    if (csv[pos++] != ';') {
        if (LOG_ENABLED) {
            Serial.print("CSV parse error: expected ';' after y: ");
            Serial.println(csv);
        }
        return;
    }

    char color = csv[pos];

    if (x >= WIDTH || y >= HEIGHT) {
        if (LOG_ENABLED) {
            Serial.print("CSV out of bounds: ");
            Serial.println(csv);
        }
        return;
    }

    strip.setPixelColor(xyToIndex(x, y), colorToRGB(color));
}


enum RxState {
    WAIT_FRAME,
    IN_FRAME
};

RxState rxState = WAIT_FRAME;

char lineBuffer[MAX_CSV_LINE_SIZE + 1];
uint8_t lineIndex = 0;

void processSerial() {
    while (Serial.available()) {
        char c = Serial.read();

        if (rxState == WAIT_FRAME) {
            if (c == '@') {
                if (LOG_ENABLED) {
                    Serial.println("Frame start");
                }
                strip.clear();
                lineIndex = 0;
                rxState = IN_FRAME;
            }
            continue;
        }

        // rxState == IN_FRAME
        if (c == '#') {
            if (LOG_ENABLED) {
                Serial.println("Frame end");
            }
            strip.show();
            rxState = WAIT_FRAME;
            lineIndex = 0;
            continue;
        }

        if (c == '\r') continue;

        if (c == '\n') {
            lineBuffer[lineIndex] = '\0';
            if (LOG_ENABLED) {
                Serial.print("CSV: ");
                Serial.println(lineBuffer);
            }
            displayCsvLine(lineBuffer);
            lineIndex = 0;
            continue;
        }

        if (lineIndex < MAX_CSV_LINE_SIZE) {
            lineBuffer[lineIndex++] = c;
        } else if (LOG_ENABLED) {
            Serial.println("CSV line too long, truncating");
        }
    }
}


void setup() {
    Serial.begin(115200);
    strip.begin();
    strip.setBrightness(32);
    strip.clear();
    strip.show();
}

void loop() {
    processSerial();
}
