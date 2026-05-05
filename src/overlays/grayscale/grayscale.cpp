#include "ap_int.h"
#include "hls_stream.h"
#include "ap_axi_sdata.h"

// 32-bit AXI stream word (padded BGR pixel in)
typedef ap_axiu<32, 0, 0, 0> StreamPixelIn;

// 8-bit AXI stream word (grayscale byte out)
typedef ap_axiu<8,  0, 0, 0> StreamPixelOut;



void grayscale(
    hls::stream<StreamPixelIn>  &stream_in,
    hls::stream<StreamPixelOut> &stream_out,
    int pixel_count   // = width * height = 307200 for 640x480
) { 

#pragma HLS INTERFACE axis      port=stream_in
#pragma HLS INTERFACE axis      port=stream_out
#pragma HLS INTERFACE s_axilite port=pixel_count
#pragma HLS INTERFACE s_axilite port=return   

    for (int i = 0; i < pixel_count; i++) { 
#pragma HLS PIPELINE II=1
        StreamPixelIn  px_in  = stream_in.read();
        StreamPixelOut px_out;

        ap_uint<8> b = (px_in.data >>  0) & 0xFF;
        ap_uint<8> g = (px_in.data >>  8) & 0xFF;
        ap_uint<8> r = (px_in.data >> 16) & 0xFF;


        // ITU-R BT.601 integer approximation (avoids floating point on FPGA)
        // Y = (29*B + 150*G + 77*R) >> 8   ≈  0.114*B + 0.587*G + 0.299*R
        ap_uint<18> gray = 29*b + 150*g + 77*r;

        px_out.data = gray >> 8;
        px_out.last = px_in.last;   // pass through end-of-frame signal
        px_out.keep = 1;
        px_out.strb = 1;

        stream_out.write(px_out);

    }
 
}