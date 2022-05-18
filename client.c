#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "fmt.h"
#include "net/gcoap.h"
#include "net/utils.h"
#include "od.h"

#include "gcoap_example.h"

#define ENABLE_DEBUG 0
#include "debug.h"

#if IS_USED(MODULE_GCOAP_DTLS)
#include "net/dsm.h"
#endif

static bool _proxied = false;
static sock_udp_ep_t _proxy_remote;
static char proxy_uri[64];

/* Retain request path to re-request if response includes block. User must not
 * start a new request (with a new path) until any blockwise transfer
 * completes or times out. */
#define _LAST_REQ_PATH_MAX (64)
static char _last_req_path[_LAST_REQ_PATH_MAX];

uint16_t req_count = 0;

static int _print_usage(char **argv)
{
    printf("usage: %s <this|is|just|a|test>\n", argv[0]);
    return 1;
}

int gcoap_cli_cmd(int argc, char **argv)
{
    /* Ordered like the RFC method code numbers, but off by 1. GET is code 0. */
    char *method_codes[] = {"ping", "get", "post", "put"};

    if (argc == 1) {
		printf("hello! this is client#23\n", argv[0]);
        return 1;
    }

    return _print_usage(argv);
}
