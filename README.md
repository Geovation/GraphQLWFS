# GraphQLWFS
A query middleware for quering WFS services

A prototype that will use GraphQL as a middletier to query WFS services.

live demo: https://us-central1-gcp-training-144309.cloudfunctions.net/graphqlwfs

encrypt variable with

```
OS_KEY=1234567890
echo -n $OS_KEY | gcloud kms encrypt --plaintext-file=- --ciphertext-file=- --location=global --keyring=projects/gcp-training-144309/locations/global/keyRings/graphQL --key=projects/gcp-training-144309/locations/global/keyRings/graphQL/cryptoKeys/live | base64`
```

To run in locally
```
OS_KEY=1234567890
./local.sh
```
