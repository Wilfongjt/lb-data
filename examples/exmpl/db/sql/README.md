
* The system is enabled by a JWT token called a woden
* The system expects to be run over an encrypted connection
* Woden is the origin
* LyttleBit is Woden
* RegisterAPI is the application and user management system API
* AdoptionAPI is an application specific API
* Adopt-a-Drain is an application
* Adopt-a-Drain uses the RegisterAPI and, AdoptionAPI APIs
* Passwords are encrypted before storage
* Passwords are never passed out of the database system
* Registered applications have an application specific token called an app-token
* Users get a temporary JWT token called a user-token
* User-tokens expire
* RegisterAPI woden API call does not require a token
* Wodens do not expire
* Wodens can be replaced


# Setup
1. Configure
   1. Environment (.env)
   2. Manually Configure woden: Run docker-compose
   3. Get a woden: Curl a worden
2. Register an Application
   1. Create an Application
   2. Check proper application creation: Curl an Application  
3. Register an Application User
   1. Create a user
   2. Check proper user creation: Curl a user
4.

## Setup
  1.1. Configure .env (place .env in folder with docker-compose.yml)
  ```
      POSTGRES_DB=application_db
      POSTGRES_USER=postgres
      POSTGRES_PASSWORD=mysecretdatabasepassword
      POSTGRES_JWT_SECRET=PASSWORDmustBEATLEAST32CHARSLONG
      LB_GUEST_PASSWORD=mysecretclientpassword
      PGRST_DB_SCHEMA=api_schema
      PGRST_DB_ANON_ROLE=api_guest
  ```

  1.2. Fireup docker-compose:
  ```
      docker-compose up
  ```

  3. Get a woden from the docker-compose start up or get one from postgres with woden()
  4. Set WODEN environment variable:
  ```
      export WODEN="<woden>"
  ```
  5. Register an application
  ```
      curl http://localhost:3100/rpc/app -X POST \
           -H "Authorization: Bearer $WODEN"   \
           -H "Content-Type: application/json" \
           -H "Prefer: params=single-object"\
           -d '{"type": "app", "name": "request@1.0.0", "group":"register", "owner": "me@someplace.com", "password": "a1A!aaaa"}'
  ```
  6. Get application-token: app('{"id":""}')
  ```
      curl http://localhost:3100/rpc/app -X POST \
           -H "Authorization: Bearer $WODEN"   \
           -H "Content-Type: application/json" \
           -d '{"id": "my_app@1.0.0"}'
  ```
  7. Set AADTOKEN environment variable:
  ```
      export AADTOKEN=<application-token>
  ```
  8. Register AAD application user (repeat as needed)
  ```
      curl http://localhost:3100/rpc/user -X POST \
           -H "Authorization: Bearer $APPTOKEN"   \
           -H "Content-Type: application/json" \
           -H "Prefer: params=single-object"\
           -d '{"type": "user", "name": "request@1.0.0", "username": "me@someplace.com", "password": "a1A!aaaa"}'

  ```
  9. Application Signin Or get user-token:
  ```
      curl http://localhost:3100/rpc/user -X POST \
           -H "Authorization: Bearer $APPTOKEN"   \
           -H "Content-Type: application/json" \
           -d '{"username":"", "password":""}'
  ```
application_db
    api_schema
        woden
        register
            app
            user
        adoptions
            adopt
roles
    api_guest
    aad_guest user
