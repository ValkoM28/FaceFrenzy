#include <iostream>
#include "grayscale.h"

int main() {
    hls::stream<StreamPixelIn>  in_stream;
    hls::stream<StreamPixelOut> out_stream;

    // Single test pixel: B=255, G=0, R=0 (pure blue)
    // Expected gray: (29*255 + 0 + 0) >> 8 = 7395 >> 8 = 28
    StreamPixelIn px;
    px.data = 0x000000FF;  // blue pixel
    px.last = 1;
    px.keep = 0xF;
    px.strb = 0xF;
    in_stream.write(px);

    grayscale(in_stream, out_stream, 1);

    StreamPixelOut result = out_stream.read();
    std::cout << "Gray value: " << (int)result.data << " (expected ~28)" << std::endl;

    return 0;
}