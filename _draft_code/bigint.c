#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* NOTES: */
/* I'm using chars instead of ints to save space. Because I'm only storing digits in them, I have enough */
/* space to store two digits per char, but I don't want to mess with bit flipping */

/* This will probably only be fixed size (even for adding), but I might fix that later :) */

struct bigint
{
    size_t num_digits;
    char* digits;
};
typedef struct bigint bigint;

/* Create a bigint from a char* and a size. */
/* produces a bigint of value 0 if digits is NULL */
/* digits should either be a char* of digits ( "11223249" ), or NULL */
/* num_digits should ALWAYS be strlen(digits) if digits != NULL */
/* TODO use a max_num_digits arg and copy back to front so I can left pad with 0s */
bigint* malloc_bigint(char* digits, size_t num_digits)
{
    // create the appropriate buffers and fill in what we can
    bigint* new_bigint = malloc(sizeof(bigint));
    new_bigint->num_digits = num_digits;

    char* new_buffer = malloc(sizeof(char) * num_digits);
    memset(new_buffer, 0, num_digits);

    if (digits)
    {
        // copy the digits into buffer converting from chars to digits
        // TODO: I should probably use strncopy (it's probably vectorized) and subtract stuff in a separate stuff
        char* current_digits_char = digits;
        char* current_new_buffer_char = new_buffer;
        for(size_t i = 0; i < num_digits; ++i)
        {
            *(current_new_buffer_char + i) = *(current_digits_char + i) - '0';
        }

    }
    new_bigint->digits = new_buffer;
    return new_bigint;
}

void free_bigint(bigint* bi)
{
    free(bi->digits);
    free(bi);
}

void printf_bigint(bigint* bi)
{
    printf("size: %zu\n", bi->num_digits);
    printf("digits: ");
    for(size_t i = 0; i < bi->num_digits; ++i)
    {
        printf("%c", bi->digits[i] + '0');
    }
    printf("\n");
}

int main()
{
    {
        bigint* a = malloc_bigint(NULL, 5);
        printf_bigint(a);
        free_bigint(a);
    }
    {
        bigint* a = malloc_bigint("12345", 5);
        printf_bigint(a);
        free_bigint(a);
    }
}
