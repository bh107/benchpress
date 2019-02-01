#pragma OPENCL EXTENSION cl_khr_fp64 : enable

__kernel void heat_eq_jacobi(uint width, uint height
                             , __global DTYPE* in
                             , __global DTYPE* out
                             , __global DTYPE* delta)
{
    uint gid = get_global_id(0);
    if (gid >= width)
        return;
    uint w = width + 2;
    uint h = height + 2;
    DTYPE d = 0.0;
    for (uint i = 0; i < height; ++i)
    {
        uint offset = i*w;
        DTYPE up     = in[gid+1+offset];
        DTYPE left   = in[gid+w+offset];
        DTYPE right  = in[gid+w+2+offset];
        DTYPE down   = in[gid+1+w*2+offset];
        DTYPE center = in[gid+w+1+offset];
        DTYPE out_center = (center + up + left + right + down) * 0.2;
        out[gid+w+1+offset] = out_center;
        d += fabs(out_center - center);
    }
    delta[gid] = d;
}
