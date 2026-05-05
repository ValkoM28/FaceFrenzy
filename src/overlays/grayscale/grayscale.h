#ifndef GRAYSCALE_H
#define GRAYSCALE_H

#include "ap_int.h"
#include "hls_stream.h"
#include "ap_axi_sdata.h"

typedef ap_axiu<32, 0, 0, 0> StreamPixelIn;
typedef ap_axiu<8,  0, 0, 0> StreamPixelOut;

void grayscale(
    hls::stream<StreamPixelIn>  &stream_in,
    hls::stream<StreamPixelOut> &stream_out,
    int pixel_count
);

#endif