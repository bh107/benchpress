#include <sys/time.h>
#include <getopt.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <bp_util.h>

size_t start, stop;

//
//  Time sampling
//
size_t bp_sample_time(void)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_usec + tv.tv_sec * 1000000;
}

size_t bp_start(void)
{
    start = bp_sample_time();
    return start;
}

size_t bp_stop(void)
{
    stop = bp_sample_time();
    return stop;
}

double bp_elapsed(void)
{
    return (stop-start)/(double)1000000.0;
}

void bp_print(const char* tool)
{
    printf("Ran %s elapsed-time: %lf\n", tool, bp_elapsed());
}

//
//  Argument parsing
//
static void parse_size(bp_arguments_type* args, char* arg)
{
    args->nsizes = 0;
    while (1) {
        char *tail;
        int next;

        while ('*'==*arg) {
            arg++;
        }
        if (*arg == 0) {
            break;
        }

        next = strtol (arg, &tail, 0);

        arg = tail;
        args->sizes[args->nsizes] = next;
        args->nsizes++;
    }
}

bp_arguments_type bp_parse_args(int argc, char** argv)
{   
    bp_arguments_type args;
    args.has_unknown = 0;
    args.has_error = 0;

    static int verbose_flag;
    static int visualize_flag;
    while (1)
    {
        static struct option long_options[] = {
            {"verbose", no_argument, &verbose_flag, 1},
            {"visualize", no_argument, &visualize_flag, 1},
            {"size",    required_argument, 0, 's'},
            {0, 0, 0, 0}
        };
        int option_index = 0;   // getopt_long stores option index here
        int c = getopt_long(argc, argv, "s:", long_options, &option_index);
        if (c == -1) {
            break;
        }

        switch (c) {
            case 0:
                if (long_options[option_index].flag != 0) {
                    break;
                }
                break;
            case 's':
                parse_size(&args, optarg);
                break;
            case '?':
                args.has_unknown = 1;
                break;
            default:
                args.has_error = 1;
                break;
        }
    }
    args.verbose = verbose_flag;
    args.visualize = visualize_flag;
    return args;
}

//
//  Wrap everything up in this thing...
//
bp_util_type bp_util_create(int argc, char** argv, int nsizes)
{
    bp_util_type util = {
        .args = bp_parse_args(argc, argv),
        .timer_start = bp_start,
        .timer_stop = bp_stop,
        .elapsed = bp_elapsed,
        .print = bp_print
    };

    if ((nsizes < 0) || (nsizes > 10)) {
        printf("bp_util_create(..., nsizes >10 or <0) this is no go.\n");
        util.args.has_error = 1;
    } else if (util.args.has_unknown || util.args.has_error || nsizes != util.args.nsizes) {
        printf("Invalid arguments, check usage\n");
        char size_descr[100];
        strcpy(size_descr, "");
        for(int i=0; i<nsizes; ++i) {
            strcat(size_descr, "NUMBER");
            if (i<nsizes-1) {
                strcat(size_descr, "*");
            }
        }
        printf("usage: %s --size=%s [--verbose]\n", argv[0], size_descr);
        util.args.has_error = 1;
    }
    
    return util;
}
