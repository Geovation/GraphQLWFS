# GraphQLWFS
A query middleware for quering WFS services

A prototype that will use GraphQL as a middletier to query WFS services.

live demo: https://us-central1-graphql-wfs.cloudfunctions.net/graphqlwfs

encrypt variable with

```
export OS_KEY=1234567890
export PROJECT=graphql-wfs
echo -n $OS_KEY | gcloud kms encrypt \
  --plaintext-file=- \
  --ciphertext-file=- \
  --location=global \
  --keyring=projects/$PROJECT/locations/global/keyRings/graphQL \
  --key=projects/$PROJECT/locations/global/keyRings/graphQL/cryptoKeys/live | base64
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
python -m unittest  --verbose # it runs the tests
python local.py # it runs a local server
```

Example:

```
curl 127.0.0.1:5000 -H "Content-Type: application/json" -d '{ hello(count: 5, propertyName: "Type", literal: "Education") }'
```

**Note 1**: As of this writing 05/02/2021, Hasura.io has a growing userbase with over 20k stars on Github and comparing with other alternatives on filter query design for GraphQL, Hasura.io documentation seem to be comprehensive and clear in design. Therefore, the query design schema has been chosen for this project to be as developer friendly as possible.