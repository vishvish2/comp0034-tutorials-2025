# 1. Introduction to Pydantic schemas and GET, CREATE, PUT/PATCH and DELETE routes

## Pydantic schema versus database models

Pydantic uses Python type hints and enforces these at runtime.

A Pydantic schema is a class definition that includes type hints for attributes and can include
field definitions.

Field definitions apply constraints such as `Field(max_length=50, ge=0, regex="^[A-Za-z]+$")`, e.g.,
limiting string length, enforcing numeric
bounds, or validating against a regular expression.

You can also customise field validators by using the `@field_validator` or `@model_validator`
decorators to implement custom validation logic, transform inputs, or enforce cross‑field rules.

FastAPI uses Pydantic schemas for validation, serialization, and automatic documentation, ensuring
that request bodies, responses, and OpenAPI docs are all consistent and type‑safe.

Although Pydantic schemas and database model classes often look similar, their purposes are
different:

**Pydantic schemas**:

- Represent the shape of data that your API expects or returns.
- Validate input data at runtime (types, constraints, custom validators).
- Control what fields are exposed to or accepted from the client (e.g., hiding passwords or DB‑only
  fields).
- Are not tied to database structure or persistence.
- Used by FastAPI for:

    - Request parsing
    - Response serialization
    - OpenAPI documentation

**ORM model classes** (e.g., SQLAlchemy models)

- Define the schema of your database tables.
- Specify column types, primary keys, relationships, indexes, and constraints that the database
  enforces.
- Govern how objects are stored, updated, and queried from the database.
- Include ORM-specific configuration such as relationship(), ForeignKey, Column, back_populates,
  etc.

### Summary

| Purpose      | Pydantic schema                           | ORM model class                                |
|:-------------|:------------------------------------------|:-----------------------------------------------|
| Defines      | API data shape                            | Database table structure                       | 
| Validates    | Input/output data                         | Constraints at database level                  |
| Used for     | Validation, serialization, docs           | Persistence and querying                       |
| FastAPI role | Request/response models                   | Data storage models                            |
| Contains     | Type hints, validators, field constraints | Column definitions, relationships, ORM mapping |

<caption>Table 1: Comparison of the roles of Pydantic schemas and ORM model classes in FastAPI apps</caption>

## GET, CREATE, PUT/PATCH, and DELETE routes

The range of routes in a REST API typically include HTTP methods:

- GET one
- GET many
- CREATE one
- PUT update one replacing all fields
- PATCH update one, partial fields
- DELETE one

Any may include others, e.g. GET based on a search criteria.

In a FastAPI app, you will have models that represent database tables and schemas that determine the
fields required in requests and responses for routes using the above HTTP methods.

For each entity in your domain model, you may have the following Python classes for the
models and schemas:

- SQLAlchemy model → database table representation (e.g., Disability).
- Pydantic schemas:

    - DisabilityBase → shared fields
    - DisabilityCreate → fields required when creating
    - DisabilityUpdate → fields required for full update (PUT)
    - DisabilityPatch → optional fields for partial update (PATCH)
    - DisabilityResponse → what you return to the client (may hide internal DB fields)

You will need a varying combination of models and schemas for each type of route, for example:

| Route                  | Uses                                                                                                                                         | Reason                                                                                                                                                                                   |
|:-----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET (list / read all)  | ORM model → for querying the database<br>Pydantic Response Schema → for returning data                                                       | GET requests don’t include a body (normally)<br>Only need to return clean, serialized data to the client<br>Response schema ensures no database‑only fields are leaked (e.g., passwords) |
| POST (create)          | Pydantic Input Schema → request body<br>ORM model → to insert into database<br>Pydantic Response Schema → return newly created object        | Creating a record needs validated input.<br>ORM model persists it.<br>Response schema shapes what is returned (e.g., hiding password hash).                                              |
| GET by ID (read one)   | ORM model → to fetch from DB<br>Response Schema → to return result                                                                           |                                                                                                                                                                                          |
| PUT (full update)      | Pydantic Update Schema → usually all required fields<br>ORM model → apply changes + save<br>Pydantic Response Schema → return updated object | PUT semantics: replace the entire resource so schema generally requires all fields<br>ORM updates the DB record                                                                          |
| PATCH (partial update) | Pydantic Patch Schema → all fields optional<br>ORM model → apply only the changed fields<br>Pydantic Response Schema → return updated object | PATCH semantics: only send fields you want to update<br>Schema fields are optional so clients can send only one or two                                                                   |
| DELETE                 | ORM model → to locate and delete the record<br>No request schema needed normally<br>Response schema optional (204 = no content usually)      | DELETE has no body<br>Database model ensures you delete the right object<br>Often return nothing (204 No Content)                                                                        |

<caption>Table 2: Mapping typical Pydantic schemas and ORM models to routes with different HTTP methods</caption>

Route operations need to be **idempotent**. An idempotent operation is one that can be performed
multiple times with the same result as if it were performed once.

In REST, this matters because clients (browsers, proxies, load balancers) may retry
requests, especially after timeouts or network issues. Idempotent methods ensure these retries don't
cause unintended effects.

| HTTP Method | Idempotent? | Explanation                                                                                                                                                       |
|:------------|:-----------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET         |     Yes     | Repeating it returns the same resource; does not change state.                                                                                                    |
| PUT         |     Yes     | Replaces a resource with the same representation each time.                                                                                                       |
| DELETE      |     Yes     | Deleting the same resource multiple times yields same state: the resource is gone.                                                                                |
| PATCH       |  Sometimes  | If PATCH sets fields instead of adding or modifying them relative to current state, then repeated calls have the same effect so in this case would be idempotent. |
| POST        |     No      | Each call usually creates something new or triggers an action.                                                                                                    |

<caption>Table 3: Idempotency and HTTP methods</caption>

## This week's activities

Last week the activities used ORM models only in the GET routes. This week's activities will add
Pydantic schemas for the models, alter the GET routes to use the response models, and then define
the remaining routes.

Note that you would provide the range of routes for all the data you want the REST API to provide.
For brevity, the activities only provide the subset needed for the dashboard/quiz app.

[Next activity](2-schemas.md)