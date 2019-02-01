#include <iostream>
#include <sys/time.h>
#include <CL/cl.hpp>
#include <stdexcept>
#include <sys/time.h>
#include <cstdio>
#include <fstream>
#include <sstream>
#include <utility>

cl::Context context;
std::vector<cl::Device> devices;
cl::CommandQueue commandQueue;
cl::Kernel kernel;

#define TPB 32
#ifndef DTYPE
#define DTYPE double
#endif
#define STR(s) #s
#define xSTR(s) STR(s)

int main (int argc, char** argv)
{
    if (argc != 5)
    {
        std::cout << "Usage: " << argv[0] << " HEAT-EQ-KERNEL-FILE WIDTH HEIGHT ITERATIONS" << std::endl;
        return 0;
    }
    // Commandline arguments
    char *opencl_file = argv[1];
    unsigned int width  = atoi(argv[2]);
    unsigned int height = atoi(argv[3]);
    unsigned int iter   = atoi(argv[4]);

    // Setup OpenCL execution system
    std::vector<cl::Platform> platforms;
    cl::Platform::get(&platforms);
    bool foundPlatform = false;
    std::vector<cl::Platform>::iterator it;
    for (it = platforms.begin(); it != platforms.end(); ++it)
    {
        try {
            cl_context_properties props[] = {CL_CONTEXT_PLATFORM, (cl_context_properties)(*it)(),0};
            context = cl::Context(CL_DEVICE_TYPE_GPU, props);
            foundPlatform = true;
            break;
        }
        catch (cl::Error e)
        {
            foundPlatform = false;
        }
    }
    if (foundPlatform)
    {
        devices = context.getInfo<CL_CONTEXT_DEVICES>();
        commandQueue = cl::CommandQueue(context,devices[0],0);
    } else {
        throw std::runtime_error("Could not find valid OpenCL platform.");
    }

    // Read source file and compile code
    std::ifstream file(opencl_file, std::ios::in);
    if (!file.is_open())
    {
        throw std::runtime_error("Could not open source file.");
    }
    std::ostringstream srcstrs;
    srcstrs << "#define DTYPE " << xSTR(DTYPE) << "\n";
    srcstrs << file.rdbuf();
    std::string srcstr = srcstrs.str();
#ifdef DEBUG
    std::cout << srcstr << std::endl;
#endif
    cl::Program::Sources source(1,std::make_pair(srcstr.c_str(),0));
    cl::Program program(context, source);
    try {program.build(devices);}
    catch (cl::Error e)
    {
        std::cout << program.getBuildInfo<CL_PROGRAM_BUILD_LOG>(devices[0]) << std::endl;
    }
    kernel = cl::Kernel(program, "heat_eq_jacobi");

    // Set up model
    unsigned int w = width+2;
    unsigned int h = height+2;
    size_t grid_size = w*h*sizeof(DTYPE);
    size_t delta_size = w*sizeof(DTYPE);
    DTYPE* grid = (DTYPE*)malloc(grid_size);
    memset(grid, 0, grid_size);
    for(int j=0; j<w;j++)
    {
        grid[j] = 40.0;
        grid[j+(h-1)*w] = -273.15;
    }
    for(int j=1; j<h-1;j++)
    {
        grid[j*w] = -273.15;
        grid[j*w+w-1]= -273.15;
    }
#ifdef DEBUG
    for (int i = 0; i<h; i++)
    {
        for(int j=0; j<w;j++)
        {
            printf ("%lf ", grid[j+i*w]);
        }
        printf ("\n");
    }
#endif
    // Start timing
    timeval t_start,t_end;
    gettimeofday(&t_start,NULL);

    // Set up buffers and copy data
    cl::Buffer inDev = cl::Buffer(context, CL_MEM_READ_WRITE, grid_size, NULL);
    cl::Buffer outDev = cl::Buffer(context, CL_MEM_READ_WRITE, grid_size, NULL);
    cl::Buffer deltaDev = cl::Buffer(context, CL_MEM_READ_WRITE, delta_size, NULL);
    cl::Buffer deltaHost = cl::Buffer(context, CL_MEM_READ_WRITE | CL_MEM_ALLOC_HOST_PTR, delta_size, NULL);
    DTYPE* deltaHostPtr = (DTYPE*)commandQueue.enqueueMapBuffer(deltaHost, CL_TRUE, CL_MAP_WRITE, 0, delta_size);
    commandQueue.enqueueWriteBuffer(inDev, CL_FALSE, 0, grid_size, grid);
    commandQueue.enqueueCopyBuffer(inDev, outDev, 0, 0, grid_size);

    // Iterating
    for(int n=0; n<iter; ++n)
    {
        kernel.setArg(0,width);
        kernel.setArg(1,height);
        kernel.setArg(2,inDev);
        kernel.setArg(3,outDev);
        kernel.setArg(4,deltaDev);
        commandQueue.enqueueNDRangeKernel(kernel, cl::NullRange,
                                          cl::NDRange((width/TPB+1)*TPB), cl::NDRange(TPB));
        commandQueue.enqueueReadBuffer(deltaDev, CL_FALSE, 0, delta_size, deltaHostPtr);
        commandQueue.finish();
        DTYPE delta = 0.0;
        for (unsigned int i = 0; i < width; ++i)
            delta += deltaHostPtr[i];
#ifdef DEBUG
        std::cout << "Delta: " << delta << std::endl;
#endif
        cl::Buffer tmp = inDev;
        inDev = outDev;
        outDev = tmp;
    }
    commandQueue.enqueueReadBuffer(inDev, CL_TRUE, 0, grid_size, grid);
    gettimeofday(&t_end,NULL);
#ifdef DEBUG
    for (int i = 0; i<h; i++)
    {
        for(int j=0; j<w;j++)
        {
            printf ("%lf ", grid[j+i*w]);
        }
        printf ("\n");
    }
#endif
    double d_time = (t_end.tv_sec - t_start.tv_sec) + (t_end.tv_usec - t_start.tv_usec)/1000000.0;
    std::cout << argv[0] << " - iter: " << iter << " size: " << width << "*" << height << " elapsed-time: " <<
        d_time << std::endl;
    return 0;
}
