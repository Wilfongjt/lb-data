
\c application_db;

CREATE SCHEMA if not exists api_schema;
---------------
-- SCHEMA: api_schema
---------------

SET search_path TO api_schema, public;
-----------------
-- FUNCTION: USER
-----------------
-- Create or Update a user
-- Role:
-- Permissions: EXECUTE
-- Returns: JSONB

CREATE OR REPLACE FUNCTION actor(form JSONB) RETURNS JSONB AS $$
  BEGIN
    -- confirm all required attributes are in form
    -- validate attribute values

    return '{"status": "200"}'::JSONB;
  END;
$$ LANGUAGE plpgsql;
-----------------
-- FUNCTION: USER_VALIDATE
-----------------
-- Permissions: EXECUTE
-- Returns: JSONB
CREATE OR REPLACE FUNCTION
actor_validate(form JSONB) RETURNS JSONB
AS $$

  BEGIN
    -- confirm all required attributes are in form
    -- validate attribute values

    return '{"status": "200"}'::JSONB;
  END;
$$ LANGUAGE plpgsql;


/*

# Create Actor
curl http://localhost:3100/rpc/actor -X POST \
     -H "Authorization: Bearer $APPTOKEN"   \
     -H "Content-Type: application/json" \
     -H "Prefer: params=single-object"\
     -d '{"id": "my_app@1.0.0"}'


*/
