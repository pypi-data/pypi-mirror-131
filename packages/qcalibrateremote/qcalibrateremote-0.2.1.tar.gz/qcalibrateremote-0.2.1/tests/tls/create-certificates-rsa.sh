#!/bin/bash

DAYS=1825
PREFIX="test"
FILENAME_CA="${PREFIX}-ca"
FILENAME_SERVER="${PREFIX}-server"
OPENSSL="/usr/bin/openssl"

$OPENSSL genrsa -out ${FILENAME_CA}.key 2048

cat <<EOF >${FILENAME_CA}.cnf
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_ca
prompt = no
[req_distinguished_name]
C = DE
O = FZJ
OU = PGI
CN = qserve test CA
[v3_ca]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
EOF

$OPENSSL req -x509 -new -nodes -key ${FILENAME_CA}.key -sha256 -days ${DAYS} -out ${FILENAME_CA}.pem -config ${FILENAME_CA}.cnf

$OPENSSL genrsa -out ${FILENAME_SERVER}.key 2048

cat <<EOF >${FILENAME_SERVER}.cnf
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no
[req_distinguished_name]
C = DE
O = FZJ
OU = PGI
CN = localhost
[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = grpc.qserve.local
DNS.2 = localhost
EOF

$OPENSSL req -new -key ${FILENAME_SERVER}.key -config ${FILENAME_SERVER}.cnf -out ${FILENAME_SERVER}.csr
$OPENSSL x509 -req -in ${FILENAME_SERVER}.csr -sha256 -days ${DAYS} -CA ${FILENAME_CA}.pem -CAkey ${FILENAME_CA}.key -CAcreateserial -extfile ${FILENAME_SERVER}.cnf -out ${FILENAME_SERVER}.pem
