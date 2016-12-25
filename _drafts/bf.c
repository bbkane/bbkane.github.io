#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ARRAY_SIZE 30

// pass in a larger data type at compile time with -DDATA_TYPE=<type>
// Ex: -DDATA_TYPE=int
#ifndef DATA_TYPE
# define DATA_TYPE char
#endif

typedef DATA_TYPE data_type;

#undef DATA_TYPE

void print_truncated_data(data_type* data)
{
    printf("truncated data:\n");
    // get the last non-zero data member
    int effective_length = ARRAY_SIZE - 1;
    while(effective_length >= 0 && data[effective_length] == 0) {
        effective_length--;
    }
    for(int i = 0; i <= effective_length; i++) {
        printf("%d ", data[i]);
    }
    printf("\n");
}

void print_all_data(data_type* data)
{
    printf("all data:\n");

    for(int i = 0; i < ARRAY_SIZE; i++) {
        printf("%d ", data[i]);
    }
    printf("\n");
}

// TOOD:
// Expand this to use '-f <file>' and input in the code itself
// Must return a null terminated string
char* get_program(int argc, char** argv)
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <code>\n", argv[0]);
        exit(1);
    }
    char* program = argv[1];
    return program;
}

int main(int argc, char** argv)
{
    /* char program[] = "++><."; */
    /* char program[] = "[[++]].."; */
    /* char program[] = "++>+++++[<+>-]>."; */
    char* program = get_program(argc, argv);
    size_t program_length = strlen(program);
    char* program_ptr = program;

    // TODO: make this 'infinite' with malloc and realloc
    // The algorithm:
    // make an array with a flag variable in the middle
    // if the data pointer ever reaches the flag variable,
    // make a new array and space the data around the flag pointer again
    // Evenly? 
    data_type data[ARRAY_SIZE] = {0};
    data_type* data_ptr = data;

    while (*program_ptr) {
        assert(data_ptr >= data);
        assert(data_ptr <= data + ARRAY_SIZE);
        assert(program_ptr >= program);
        // TODO: this may need a +1 to account for the \0 appended
        assert(program_ptr <= program + program_length);

        if (*program_ptr == '>') { data_ptr++; }
        else if (*program_ptr == '<') { data_ptr--; }
        else if (*program_ptr == '+') { (*data_ptr)++; }
        else if (*program_ptr == '-') { (*data_ptr)--; }
        // TODO: replace %d with %c to print characters
        else if (*program_ptr == '.') { printf("%d\n", *data_ptr); }
        else if (*program_ptr == ',') { *data_ptr = getchar(); }
        else if (*program_ptr == '[') {
            if (!(*data_ptr)) {
                int pair_count = 1;
                while (pair_count) {
                    program_ptr++;
                    if (*program_ptr == '[') { pair_count++; }
                    if (*program_ptr == ']') { pair_count--; }
                    assert(program_ptr >= program);
                    // TODO: this may need a +1 to account for the \0 appended
                    assert(program_ptr <= program + program_length);
                }
            }
        }
        else if (*program_ptr == ']') {
            if (*data_ptr) {
                int pair_count = 1;
                while (pair_count) {
                    program_ptr--;
                    if (*program_ptr == ']') { pair_count++; }
                    if (*program_ptr == '[') { pair_count--; }
                    assert(program_ptr >= program);
                    // TODO: this may need a +1 to account for the \0 appended
                    assert(program_ptr <= program + program_length);
                }
            }
        }
        program_ptr++;
    }
    print_truncated_data(data);
    print_all_data(data);
}

