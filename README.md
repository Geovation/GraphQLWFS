# GraphQLWFS
A query middleware for quering WFS services

A prototype that will use GraphQL as a middletier to query WFS services.

live demo: https://us-central1-gcp-training-144309.cloudfunctions.net/graphqlwfs

encrypt variable with

```
export OS_KEY=1234567890
echo -n $OS_KEY | gcloud kms encrypt \
  --plaintext-file=- \  # - reads from stdin
  --ciphertext-file=- \  # - writes to stdout
  --location=global \
  --keyring=projects/gcp-training-144309/locations/global/keyRings/graphQL \
  --key=projects/gcp-training-144309/locations/global/keyRings/graphQL/cryptoKeys/live | base64
```

To run test.py
Type the following command in the command prompt
```
python test.py
```

To run in locally (without GCP tools)
```
echo OS_KEY=1234567890 > .env 
docker-compose up
```

To run it locally (without GCP tools not docker)
```
python3 -m venv venv
export OS_KEY=1234567890
source venv/bin/activate
python -m pip install -r requirements.txt
python main_test.py # it runs the tests
python main.py # it runs a local server
```

Example:

```
curl 127.0.0.1:5000 -H "Content-Type: application/json" -d '{ hello(count: 5, propertyName: "Type", literal: "Education") }'
```
