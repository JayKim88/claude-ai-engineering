# API Design: {{PROJECT_NAME}}

**Version:** {{API_VERSION}}
**Date:** {{DATE}}
**API Lead:** {{API_LEAD}}

---

## API Overview

**Base URL:** {{API_BASE_URL}}
**API Style:** {{API_STYLE}}
**Protocol:** {{API_PROTOCOL}}
**Data Format:** {{API_DATA_FORMAT}}

**Purpose:**
{{API_PURPOSE}}

---

## Authentication

### Authentication Method

**Type:** {{AUTH_TYPE}}
**Token Format:** {{TOKEN_FORMAT}}
**Token Location:** {{TOKEN_LOCATION}}

**Authentication Flow:**
1. {{AUTH_STEP_1}}
2. {{AUTH_STEP_2}}
3. {{AUTH_STEP_3}}
4. {{AUTH_STEP_4}}

### Authentication Endpoints

#### POST /auth/register

**Purpose:** {{REGISTER_PURPOSE}}

**Request:**
```json
{
  "email": "{{EMAIL_EXAMPLE}}",
  "password": "{{PASSWORD_EXAMPLE}}",
  "name": "{{NAME_EXAMPLE}}",
  "{{REGISTER_FIELD_1}}": "{{REGISTER_VALUE_1}}"
}
```

**Response (201):**
```json
{
  "user": {
    "id": "{{USER_ID}}",
    "email": "{{EMAIL_EXAMPLE}}",
    "name": "{{NAME_EXAMPLE}}",
    "createdAt": "{{CREATED_AT}}"
  },
  "token": "{{JWT_TOKEN}}",
  "expiresIn": {{TOKEN_EXPIRY}}
}
```

**Errors:**
- 400: {{ERROR_400_REGISTER}}
- 409: {{ERROR_409_REGISTER}}

---

#### POST /auth/login

**Purpose:** {{LOGIN_PURPOSE}}

**Request:**
```json
{
  "email": "{{EMAIL_EXAMPLE}}",
  "password": "{{PASSWORD_EXAMPLE}}"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "{{USER_ID}}",
    "email": "{{EMAIL_EXAMPLE}}",
    "name": "{{NAME_EXAMPLE}}"
  },
  "token": "{{JWT_TOKEN}}",
  "refreshToken": "{{REFRESH_TOKEN}}",
  "expiresIn": {{TOKEN_EXPIRY}}
}
```

**Errors:**
- 400: {{ERROR_400_LOGIN}}
- 401: {{ERROR_401_LOGIN}}

---

#### POST /auth/refresh

**Purpose:** {{REFRESH_PURPOSE}}

**Request:**
```json
{
  "refreshToken": "{{REFRESH_TOKEN}}"
}
```

**Response (200):**
```json
{
  "token": "{{NEW_JWT_TOKEN}}",
  "expiresIn": {{TOKEN_EXPIRY}}
}
```

**Errors:**
- 401: {{ERROR_401_REFRESH}}

---

#### POST /auth/logout

**Purpose:** {{LOGOUT_PURPOSE}}

**Headers:**
```
Authorization: Bearer {{JWT_TOKEN}}
```

**Response (204):**
```
No Content
```

---

## Endpoints

### Resource: {{RESOURCE_1_NAME}}

#### GET /{{RESOURCE_1_PATH}}

**Purpose:** {{RESOURCE_1_GET_ALL_PURPOSE}}

**Authentication:** {{RESOURCE_1_GET_ALL_AUTH}}

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| {{PARAM_1}} | {{PARAM_1_TYPE}} | {{PARAM_1_REQ}} | {{PARAM_1_DEFAULT}} | {{PARAM_1_DESC}} |
| {{PARAM_2}} | {{PARAM_2_TYPE}} | {{PARAM_2_REQ}} | {{PARAM_2_DEFAULT}} | {{PARAM_2_DESC}} |
| {{PARAM_3}} | {{PARAM_3_TYPE}} | {{PARAM_3_REQ}} | {{PARAM_3_DEFAULT}} | {{PARAM_3_DESC}} |
| page | integer | No | 1 | Page number |
| limit | integer | No | 20 | Items per page |
| sort | string | No | -createdAt | Sort field and order |

**Request Example:**
```
GET /{{RESOURCE_1_PATH}}?page=1&limit=20&{{PARAM_1}}={{PARAM_1_EXAMPLE}}
Authorization: Bearer {{JWT_TOKEN}}
```

**Response (200):**
```json
{
  "data": [
    {
      "id": "{{ITEM_ID}}",
      "{{FIELD_1}}": "{{VALUE_1}}",
      "{{FIELD_2}}": "{{VALUE_2}}",
      "{{FIELD_3}}": {{VALUE_3}},
      "createdAt": "{{CREATED_AT}}",
      "updatedAt": "{{UPDATED_AT}}"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": {{TOTAL_ITEMS}},
    "totalPages": {{TOTAL_PAGES}}
  }
}
```

**Errors:**
- 400: {{ERROR_400_GET_ALL}}
- 401: {{ERROR_401_GET_ALL}}
- 403: {{ERROR_403_GET_ALL}}

---

#### GET /{{RESOURCE_1_PATH}}/:id

**Purpose:** {{RESOURCE_1_GET_ONE_PURPOSE}}

**Authentication:** {{RESOURCE_1_GET_ONE_AUTH}}

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | {{ID_DESCRIPTION}} |

**Request Example:**
```
GET /{{RESOURCE_1_PATH}}/{{ITEM_ID_EXAMPLE}}
Authorization: Bearer {{JWT_TOKEN}}
```

**Response (200):**
```json
{
  "id": "{{ITEM_ID}}",
  "{{FIELD_1}}": "{{VALUE_1}}",
  "{{FIELD_2}}": "{{VALUE_2}}",
  "{{FIELD_3}}": {{VALUE_3}},
  "{{FIELD_4}}": {
    "{{NESTED_FIELD_1}}": "{{NESTED_VALUE_1}}",
    "{{NESTED_FIELD_2}}": "{{NESTED_VALUE_2}}"
  },
  "createdAt": "{{CREATED_AT}}",
  "updatedAt": "{{UPDATED_AT}}"
}
```

**Errors:**
- 401: {{ERROR_401_GET_ONE}}
- 403: {{ERROR_403_GET_ONE}}
- 404: {{ERROR_404_GET_ONE}}

---

#### POST /{{RESOURCE_1_PATH}}

**Purpose:** {{RESOURCE_1_CREATE_PURPOSE}}

**Authentication:** {{RESOURCE_1_CREATE_AUTH}}

**Request Body:**
```json
{
  "{{FIELD_1}}": "{{VALUE_1}}",
  "{{FIELD_2}}": "{{VALUE_2}}",
  "{{FIELD_3}}": {{VALUE_3}},
  "{{FIELD_4}}": {
    "{{NESTED_FIELD_1}}": "{{NESTED_VALUE_1}}",
    "{{NESTED_FIELD_2}}": "{{NESTED_VALUE_2}}"
  }
}
```

**Validation Rules:**
- {{FIELD_1}}: {{FIELD_1_VALIDATION}}
- {{FIELD_2}}: {{FIELD_2_VALIDATION}}
- {{FIELD_3}}: {{FIELD_3_VALIDATION}}

**Response (201):**
```json
{
  "id": "{{NEW_ITEM_ID}}",
  "{{FIELD_1}}": "{{VALUE_1}}",
  "{{FIELD_2}}": "{{VALUE_2}}",
  "{{FIELD_3}}": {{VALUE_3}},
  "createdAt": "{{CREATED_AT}}",
  "updatedAt": "{{UPDATED_AT}}"
}
```

**Errors:**
- 400: {{ERROR_400_CREATE}}
- 401: {{ERROR_401_CREATE}}
- 403: {{ERROR_403_CREATE}}
- 409: {{ERROR_409_CREATE}}

---

#### PUT /{{RESOURCE_1_PATH}}/:id

**Purpose:** {{RESOURCE_1_UPDATE_PURPOSE}}

**Authentication:** {{RESOURCE_1_UPDATE_AUTH}}

**Request Body:**
```json
{
  "{{FIELD_1}}": "{{VALUE_1_UPDATED}}",
  "{{FIELD_2}}": "{{VALUE_2_UPDATED}}",
  "{{FIELD_3}}": {{VALUE_3_UPDATED}}
}
```

**Response (200):**
```json
{
  "id": "{{ITEM_ID}}",
  "{{FIELD_1}}": "{{VALUE_1_UPDATED}}",
  "{{FIELD_2}}": "{{VALUE_2_UPDATED}}",
  "{{FIELD_3}}": {{VALUE_3_UPDATED}},
  "updatedAt": "{{UPDATED_AT}}"
}
```

**Errors:**
- 400: {{ERROR_400_UPDATE}}
- 401: {{ERROR_401_UPDATE}}
- 403: {{ERROR_403_UPDATE}}
- 404: {{ERROR_404_UPDATE}}

---

#### PATCH /{{RESOURCE_1_PATH}}/:id

**Purpose:** {{RESOURCE_1_PATCH_PURPOSE}}

**Authentication:** {{RESOURCE_1_PATCH_AUTH}}

**Request Body:**
```json
{
  "{{FIELD_1}}": "{{VALUE_1_PATCHED}}"
}
```

**Response (200):**
```json
{
  "id": "{{ITEM_ID}}",
  "{{FIELD_1}}": "{{VALUE_1_PATCHED}}",
  "{{FIELD_2}}": "{{VALUE_2}}",
  "{{FIELD_3}}": {{VALUE_3}},
  "updatedAt": "{{UPDATED_AT}}"
}
```

**Errors:**
- 400: {{ERROR_400_PATCH}}
- 401: {{ERROR_401_PATCH}}
- 403: {{ERROR_403_PATCH}}
- 404: {{ERROR_404_PATCH}}

---

#### DELETE /{{RESOURCE_1_PATH}}/:id

**Purpose:** {{RESOURCE_1_DELETE_PURPOSE}}

**Authentication:** {{RESOURCE_1_DELETE_AUTH}}

**Response (204):**
```
No Content
```

**Errors:**
- 401: {{ERROR_401_DELETE}}
- 403: {{ERROR_403_DELETE}}
- 404: {{ERROR_404_DELETE}}

---

### Resource: {{RESOURCE_2_NAME}}

#### GET /{{RESOURCE_2_PATH}}

**Purpose:** {{RESOURCE_2_GET_ALL_PURPOSE}}

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| {{R2_PARAM_1}} | {{R2_PARAM_1_TYPE}} | {{R2_PARAM_1_REQ}} | {{R2_PARAM_1_DEFAULT}} | {{R2_PARAM_1_DESC}} |
| {{R2_PARAM_2}} | {{R2_PARAM_2_TYPE}} | {{R2_PARAM_2_REQ}} | {{R2_PARAM_2_DEFAULT}} | {{R2_PARAM_2_DESC}} |

**Response (200):**
```json
{
  "data": [
    {
      "id": "{{R2_ITEM_ID}}",
      "{{R2_FIELD_1}}": "{{R2_VALUE_1}}",
      "{{R2_FIELD_2}}": "{{R2_VALUE_2}}"
    }
  ]
}
```

---

#### POST /{{RESOURCE_2_PATH}}

**Purpose:** {{RESOURCE_2_CREATE_PURPOSE}}

**Request Body:**
```json
{
  "{{R2_FIELD_1}}": "{{R2_VALUE_1}}",
  "{{R2_FIELD_2}}": "{{R2_VALUE_2}}"
}
```

**Response (201):**
```json
{
  "id": "{{R2_NEW_ID}}",
  "{{R2_FIELD_1}}": "{{R2_VALUE_1}}",
  "{{R2_FIELD_2}}": "{{R2_VALUE_2}}",
  "createdAt": "{{CREATED_AT}}"
}
```

---

### Resource: {{RESOURCE_3_NAME}}

#### GET /{{RESOURCE_3_PATH}}

**Purpose:** {{RESOURCE_3_GET_ALL_PURPOSE}}

**Response (200):**
```json
{
  "data": [
    {
      "id": "{{R3_ITEM_ID}}",
      "{{R3_FIELD_1}}": "{{R3_VALUE_1}}",
      "{{R3_FIELD_2}}": {{R3_VALUE_2}}
    }
  ]
}
```

---

## Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "error": {
    "code": "{{ERROR_CODE}}",
    "message": "{{ERROR_MESSAGE}}",
    "details": [
      {
        "field": "{{FIELD_NAME}}",
        "message": "{{FIELD_ERROR_MESSAGE}}"
      }
    ],
    "requestId": "{{REQUEST_ID}}",
    "timestamp": "{{TIMESTAMP}}"
  }
}
```

### HTTP Status Codes

| Code | Name | Usage |
|------|------|-------|
| 200 | OK | {{STATUS_200}} |
| 201 | Created | {{STATUS_201}} |
| 204 | No Content | {{STATUS_204}} |
| 400 | Bad Request | {{STATUS_400}} |
| 401 | Unauthorized | {{STATUS_401}} |
| 403 | Forbidden | {{STATUS_403}} |
| 404 | Not Found | {{STATUS_404}} |
| 409 | Conflict | {{STATUS_409}} |
| 422 | Unprocessable Entity | {{STATUS_422}} |
| 429 | Too Many Requests | {{STATUS_429}} |
| 500 | Internal Server Error | {{STATUS_500}} |
| 503 | Service Unavailable | {{STATUS_503}} |

### Common Error Codes

| Code | Message | Action |
|------|---------|--------|
| {{ERR_CODE_1}} | {{ERR_MSG_1}} | {{ERR_ACTION_1}} |
| {{ERR_CODE_2}} | {{ERR_MSG_2}} | {{ERR_ACTION_2}} |
| {{ERR_CODE_3}} | {{ERR_MSG_3}} | {{ERR_ACTION_3}} |
| {{ERR_CODE_4}} | {{ERR_MSG_4}} | {{ERR_ACTION_4}} |
| {{ERR_CODE_5}} | {{ERR_MSG_5}} | {{ERR_ACTION_5}} |

---

## Rate Limiting

**Strategy:** {{RATE_LIMIT_STRATEGY}}

### Rate Limit Tiers

| Tier | Requests per Minute | Requests per Hour | Requests per Day |
|------|---------------------|-------------------|------------------|
| {{TIER_1}} | {{TIER_1_PER_MIN}} | {{TIER_1_PER_HOUR}} | {{TIER_1_PER_DAY}} |
| {{TIER_2}} | {{TIER_2_PER_MIN}} | {{TIER_2_PER_HOUR}} | {{TIER_2_PER_DAY}} |
| {{TIER_3}} | {{TIER_3_PER_MIN}} | {{TIER_3_PER_HOUR}} | {{TIER_3_PER_DAY}} |

### Rate Limit Headers

```
X-RateLimit-Limit: {{LIMIT}}
X-RateLimit-Remaining: {{REMAINING}}
X-RateLimit-Reset: {{RESET_TIMESTAMP}}
```

**Exceeded Response (429):**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "{{RATE_LIMIT_MESSAGE}}",
    "retryAfter": {{RETRY_AFTER_SECONDS}}
  }
}
```

---

## Pagination

**Default Page Size:** {{DEFAULT_PAGE_SIZE}}
**Max Page Size:** {{MAX_PAGE_SIZE}}

**Query Parameters:**
- `page`: Page number (1-indexed)
- `limit`: Items per page
- `sort`: Sort field with optional `-` prefix for descending

**Response Format:**
```json
{
  "data": [...],
  "pagination": {
    "page": {{CURRENT_PAGE}},
    "limit": {{ITEMS_PER_PAGE}},
    "total": {{TOTAL_ITEMS}},
    "totalPages": {{TOTAL_PAGES}},
    "hasNext": {{HAS_NEXT}},
    "hasPrev": {{HAS_PREV}}
  }
}
```

---

## Filtering & Sorting

### Filtering

**Supported Operators:**

| Operator | Symbol | Example |
|----------|--------|---------|
| Equals | `=` | `?status=active` |
| Not Equals | `!=` | `?status!=deleted` |
| Greater Than | `>` | `?price>100` |
| Less Than | `<` | `?price<500` |
| Greater or Equal | `>=` | `?rating>=4` |
| Less or Equal | `<=` | `?rating<=5` |
| In | `in` | `?category[in]=tech,health` |
| Contains | `~` | `?name~search` |

### Sorting

**Format:** `?sort=field1,-field2`
- `field`: Ascending order
- `-field`: Descending order

**Examples:**
- `?sort=createdAt`: Sort by creation date (oldest first)
- `?sort=-createdAt`: Sort by creation date (newest first)
- `?sort=name,-createdAt`: Sort by name (A-Z), then by date (newest first)

---

## Versioning Strategy

**Strategy:** {{VERSIONING_STRATEGY}}

**Current Version:** {{CURRENT_API_VERSION}}

**Version Format:**
{{VERSION_FORMAT}}

**Version Header:**
```
Accept: application/vnd.{{API_NAME}}.{{VERSION}}+json
```

**Deprecation Policy:**
{{DEPRECATION_POLICY}}

**Sunset Header:**
```
Sunset: {{SUNSET_DATE}}
Deprecation: {{DEPRECATION_DATE}}
Link: <{{NEW_VERSION_URL}}>; rel="successor-version"
```

---

## Webhooks

**Supported Events:**

| Event | Payload | Description |
|-------|---------|-------------|
| {{WEBHOOK_EVENT_1}} | {{WEBHOOK_PAYLOAD_1}} | {{WEBHOOK_DESC_1}} |
| {{WEBHOOK_EVENT_2}} | {{WEBHOOK_PAYLOAD_2}} | {{WEBHOOK_DESC_2}} |
| {{WEBHOOK_EVENT_3}} | {{WEBHOOK_PAYLOAD_3}} | {{WEBHOOK_DESC_3}} |

**Webhook Payload Format:**
```json
{
  "event": "{{EVENT_NAME}}",
  "timestamp": "{{TIMESTAMP}}",
  "data": {
    {{EVENT_DATA}}
  },
  "webhookId": "{{WEBHOOK_ID}}"
}
```

**Security:**
{{WEBHOOK_SECURITY}}

**Retry Policy:**
{{WEBHOOK_RETRY}}

---

## Request/Response Examples

### Example 1: {{EXAMPLE_1_NAME}}

**Scenario:** {{EXAMPLE_1_SCENARIO}}

**Request:**
```http
{{EXAMPLE_1_METHOD}} {{EXAMPLE_1_PATH}}
Authorization: Bearer {{JWT_TOKEN}}
Content-Type: application/json

{{EXAMPLE_1_REQUEST_BODY}}
```

**Response:**
```http
HTTP/1.1 {{EXAMPLE_1_STATUS}}
Content-Type: application/json

{{EXAMPLE_1_RESPONSE_BODY}}
```

---

### Example 2: {{EXAMPLE_2_NAME}}

**Scenario:** {{EXAMPLE_2_SCENARIO}}

**Request:**
```http
{{EXAMPLE_2_METHOD}} {{EXAMPLE_2_PATH}}
Authorization: Bearer {{JWT_TOKEN}}

{{EXAMPLE_2_REQUEST_BODY}}
```

**Response:**
```http
HTTP/1.1 {{EXAMPLE_2_STATUS}}
Content-Type: application/json

{{EXAMPLE_2_RESPONSE_BODY}}
```

---

## API Documentation

**Interactive Docs:** {{API_DOCS_URL}}
**OpenAPI Spec:** {{OPENAPI_SPEC_URL}}
**Postman Collection:** {{POSTMAN_COLLECTION_URL}}

**SDKs:**
- JavaScript: {{SDK_JS_URL}}
- Python: {{SDK_PYTHON_URL}}
- {{SDK_OTHER}}: {{SDK_OTHER_URL}}

---

## Testing

**Sandbox URL:** {{SANDBOX_URL}}
**Test Credentials:** {{TEST_CREDENTIALS}}
**Test Data:** {{TEST_DATA_INFO}}

**Mock Server:** {{MOCK_SERVER_URL}}

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| {{CHANGELOG_V1}} | {{CHANGELOG_D1}} | {{CHANGELOG_C1}} |
| {{CHANGELOG_V2}} | {{CHANGELOG_D2}} | {{CHANGELOG_C2}} |
| {{CHANGELOG_V3}} | {{CHANGELOG_D3}} | {{CHANGELOG_C3}} |
