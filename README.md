# GBM Software Engineer Challenge
### Roberto de Jesús García

## API Docs
`http://0.0.0.0:8000/docs`

## Getting Started
* `make up`: to bring up a local docker network running the application and services.
* `make down`: cleanup all the containers.
* `make test`: With the containers running we can also run project unit tests with coverage report.
* `make logs`: show all containers logs.

## DB migrations
`dbmate` makes easy for us to run database migrations regardless of what our backend looks like. After installing dbmate, we’ll make our first migration:
* `dbmate new <migration_name>`

This will create a new file with a name that looks like: `20230101004439_<migration_name>.sql`

## Auth0
We are using `Auth0` to protect our API. The following values must be setting on `.env`file.
* `DOMAIN`: your.domain.auth0.com
* `API_AUDIENCE`: your.api.audience
* `ALGORITHMS`: RS256 as default value

You can use a curl POST request to Auth0's oauth/token endpoint to get the access token:
    ```
    curl --request POST \
      --url https://dev-i0ib3uir.jp.auth0.com/oauth/token \
      --header 'content-type: application/json' \
      --data '{"client_id":"ktR7nwI1TV5166MoWkgci1vv8zgijbvT","client_secret":"9D5TSEXC5kvt0nl5t-BkJnmR_zcOCVwfCDQd3EtTvgTAo7XxE0Pbd6-WTp-vtVMM","audience":"https://dev-i0ib3uir.jp.auth0.com/api/v2/","grant_type":"client_credentials"}'
    ```
