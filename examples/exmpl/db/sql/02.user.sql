/*
Setup
  1. configure .env
  2. fireup docker-compose
  3. get a woden from the docker-compose start up or get one from 
  Get a Woden token

  export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJMeXR0bGVCaXQiLCJzdWIiOiJhZG1pbmlzdHJhdGUiLCJyb2xlIjoiYXBpX2d1ZXN0IiwidHlwZSI6ImFwcCJ9.B_v1zTCMlWCZ3K9yLG_MmHucZLEz0TI7-28nYL9t21M"
  fire up docker-compose

*/
\c application_db;

CREATE SCHEMA if not exists api_schema;

-----------------
-- FUNCTION: APP_VALIDATE
-----------------
-- Permissions: EXECUTE
-- Returns: BOOLEAN
CREATE OR REPLACE FUNCTION
user_validate(form JSONB) RETURNS JSONB
AS $$

  BEGIN
    -- confirm all required attributes are in form
    -- validate attribute values

    return '{"status": "200"}'::JSONB;
  END;
$$ LANGUAGE plpgsql;


/*

# GET APP success with good attributes, values and token
curl http://localhost:3100/rpc/app -X POST \
     -H "Authorization: Bearer $TOKEN"   \
     -H "Content-Type: application/json" \
     -d '{"id": "my_app@1.0.0"}'

# GET APP success with BAD attributes, values and token
curl http://localhost:3100/rpc/app -X POST \
    -H "Authorization: Bearer $BADTOKEN"   \
    -H "Content-Type: application/json" \
    -d '{"id": "my_app@1.0.0"}'
*/
