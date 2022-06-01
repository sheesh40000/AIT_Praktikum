#include <stdio.h>
#include "msg.h"

#include "net/gcoap.h"
#include "shell.h"

#include "gcoap_example.h"

#include "saulcoap.h"

#define MAIN_QUEUE_SIZE (4)
static msg_t _main_msg_queue[MAIN_QUEUE_SIZE];

static const shell_command_t shell_commands[] = {
    { "coap", "CoAP example", gcoap_cli_cmd },
    { "led", "led test", led_test_class },
    { NULL, NULL, NULL }
};

int main(void)
{
    puts("Welcome to TESTAPP!\n");
    puts("Type `help` for help, type `saul` to see all SAUL devices\n");

    msg_init_queue(_main_msg_queue, MAIN_QUEUE_SIZE);
    server_init();
    
    char line_buf[SHELL_DEFAULT_BUFSIZE];
    shell_run(shell_commands, line_buf, SHELL_DEFAULT_BUFSIZE);

    return 0;
}
