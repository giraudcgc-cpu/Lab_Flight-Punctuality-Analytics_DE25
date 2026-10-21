# --- SH script generated from LLM for public and private keys for the dashboard --- 

set -euo pipefail

KEY_DIR="${HOME}/.snowflake_keys/flight_punctuality"
USER_NAME="flight_reporter_user"
mkdir -p "${KEY_DIR}"

if [[ -f "${KEY_DIR}/${USER_NAME}.p8" ]]; then
    echo "key for ${USER_NAME} already exists - not creating a new one"
else
    # private key (unencrypted PKCS8) and the matching public key
    openssl genrsa 2048 2>/dev/null | openssl pkcs8 -topk8 -inform PEM -out "${KEY_DIR}/${USER_NAME}.p8" -nocrypt
    openssl rsa -in "${KEY_DIR}/${USER_NAME}.p8" -pubout -out "${KEY_DIR}/${USER_NAME}.pub" 2>/dev/null
fi

echo
echo "Private key (put this path in .env -> REPORTER_SNOWFLAKE_PRIVATE_KEY_PATH):"
echo "  ${KEY_DIR}/${USER_NAME}.p8"
echo
echo "== Public key: paste into dashboard/worksheets_snowflake/02_setup_user.sql =="
grep -v "PUBLIC KEY" "${KEY_DIR}/${USER_NAME}.pub" | tr -d '\n'
echo
