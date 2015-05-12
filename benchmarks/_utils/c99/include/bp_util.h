#ifndef BP_UTIL
typedef struct bp_arguments {
    int nsizes;
    int sizes[16];
    int verbose;
    int visualize;
    int has_unknown;
    int has_error;
} bp_arguments_type;

typedef struct bp_util {
    bp_arguments_type args;
    size_t (*timer_start)(void);
    size_t (*timer_stop)(void);
    double (*elapsed)(void);
    void (*print)(const char*);
} bp_util_type;

bp_arguments_type bp_parse_args(int argc, char* argv[]);
size_t bp_sample_time(void);
size_t bp_start(void);
size_t bp_stop(void);
double bp_elapsed(void);
void bp_print(const char* tool);
bp_util_type bp_util_create(int argc, char* argv[], int nsizes);
#endif
