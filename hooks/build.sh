#!/usr/bin/env sh

echo "Hooks build started"

# FIREBASE_ENV is to big to be used directly as --build-arg, creating a file which will be available for the Dockerfile
echo "Generating firebase client info..."
echo '{
  "type": "service_account",
  "project_id": "$PROJECT_ID",
  "private_key_id": "$PRIVATE_KEY_ID",
  "private_key": "$PRIVATE_KEY",
  "client_email": "$CLIENT_EMAIL",
  "client_id": "$CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "$CLIENT_X509_CERT_URL"
}' > wind-info-firebase-adminsdk-tfxe3-aa9146d5b8.json.secret

docker build --build-arg BOT_TOKEN=$BOT_TOKEN \
    --build-arg WIND_ALERT_GROUP_CHAT_ID=$WIND_ALERT_GROUP_CHAT_ID \
    -t $IMAGE_NAME .

echo "Hooks build ended"