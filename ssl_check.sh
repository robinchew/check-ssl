#!/bin/bash

# Run the openssl command and capture its output
openssl s_client -connect ciaobella.obsi.com.au:443 -servername ciaobella.obsi.com.au | openssl x509 -noout -dates
