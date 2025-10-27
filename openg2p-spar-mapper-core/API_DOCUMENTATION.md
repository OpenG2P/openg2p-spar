# API Documentation

## Base Response Format

All API responses follow the G2P Connect standard format:

```json
{
  "response_header": {
    "version": "1.0.0",
    "message": "Operation successful",
    "action": "link|resolve|update|unlink",
    "correlation_id": "uuid-string",
    "timestamp": "2024-01-01T00:00:00Z",
    "status": "success|error"
  },
  "response_body": {
    "response_payload": {
      // Operation-specific payload
    }
  }
}
```

---

## Link API

**Endpoint**: `POST /link`

Creates a mapping between a Beneficiary ID and Financial Account.

### Request

```json
{
  "request_header": {
    "version": "1.0.0",
    "message": "Link Request",
    "action": "link",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "request_body": {
    "request_payload": {
      "link_request": [
        {
          "reference_id": "ref123",
          "id": "ID123",
          "fa": "FA456",
          "name": "John Doe",
          "phone_number": "+1234567890"
        }
      ]
    }
  }
}
```

### Response (Success)

```json
{
  "response_header": {
    "version": "1.0.0",
    "message": "Link successful",
    "action": "link",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z",
    "status": "success"
  },
  "response_body": {
    "response_payload": {
      "link_response": [
        {
          "reference_id": "ref123",
          "id": "ID123",
          "fa": "FA456",
          "status": "success"
        }
      ]
    }
  }
}
```

### cURL Example

```bash
curl -X POST http://localhost:8004/link \
  -H "Content-Type: application/json" \
  -d '{
    "request_header": {
      "version": "1.0.0",
      "message": "Link Request",
      "action": "link",
      "correlation_id": "uuid",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    "request_body": {
      "request_payload": {
        "link_request": [{
          "reference_id": "ref123",
          "id": "ID123",
          "fa": "FA456",
          "name": "John Doe",
          "phone_number": "+1234567890"
        }]
      }
    }
  }'
```

---

## Resolve API

**Endpoint**: `POST /resolve`

Retrieves FA information for a given Beneficiary ID.

### Request

```json
{
  "request_header": {
    "version": "1.0.0",
    "message": "Resolve Request",
    "action": "resolve",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "request_body": {
    "request_payload": {
      "resolve_request": [
        {
          "reference_id": "ref123",
          "id": "ID123"
        }
      ]
    }
  }
}
```

### Response (Success)

```json
{
  "response_header": {
    "version": "1.0.0",
    "message": "Resolve successful",
    "action": "resolve",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z",
    "status": "success"
  },
  "response_body": {
    "response_payload": {
      "resolve_response": [
        {
          "reference_id": "ref123",
          "id": "ID123",
          "fa": "FA456",
          "name": "John Doe",
          "status": "success"
        }
      ]
    }
  }
}
```

---

## Update API

**Endpoint**: `POST /update`

Modifies an existing ID-FA mapping.

### Request

```json
{
  "request_header": {
    "version": "1.0.0",
    "message": "Update Request",
    "action": "update",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "request_body": {
    "request_payload": {
      "update_request": [
        {
          "reference_id": "ref123",
          "id": "ID123",
          "fa": "FA789",
          "name": "Jane Doe"
        }
      ]
    }
  }
}
```

---

## Unlink API

**Endpoint**: `POST /unlink`

Removes a mapping between ID and FA.

### Request

```json
{
  "request_header": {
    "version": "1.0.0",
    "message": "Unlink Request",
    "action": "unlink",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "request_body": {
    "request_payload": {
      "unlink_request": [
        {
          "reference_id": "ref123",
          "id": "ID123",
          "fa": "FA456"
        }
      ]
    }
  }
}
```

---

## DFSP Provider APIs

### Get All Providers

**Endpoint**: `GET /dfsp/providers`

Returns all provider types.

```bash
curl http://localhost:8004/dfsp/providers
```

### Get Provider by Type

**Endpoint**: `GET /dfsp/providers/{provider_type}`

Returns specific provider type (BANK, EMAIL_WALLET, MOBILE_WALLET).

```bash
curl http://localhost:8004/dfsp/providers/BANK
```

### Get Provider Values

**Endpoint**: `GET /dfsp/providers/{provider_type}/values`

Returns all values for a provider type with optional parent filtering.

```bash
curl http://localhost:8004/dfsp/providers/BANK/values
curl http://localhost:8004/dfsp/providers/BANK/values?parent_id=1
```

### Get Provider by Code

**Endpoint**: `GET /dfsp/values/{code}`

Returns provider value by code.

```bash
curl http://localhost:8004/dfsp/values/ICIC
```

### Get Children

**Endpoint**: `GET /dfsp/values/{parent_id}/children`

Returns hierarchical children (e.g., branches of a bank).

```bash
curl http://localhost:8004/dfsp/values/1/children
```

---

## Error Handling

### Error Response Format

```json
{
  "response_header": {
    "version": "1.0.0",
    "message": "Operation failed",
    "action": "link",
    "correlation_id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z",
    "status": "error"
  },
  "response_body": {
    "response_payload": {
      "error": {
        "code": "rjct_invalid_id",
        "message": "Invalid ID format"
      }
    }
  }
}
```

### Error Codes

| Code | Meaning |
|------|---------|
| `rjct_invalid_id` | Invalid ID format |
| `rjct_invalid_fa` | Invalid FA format |
| `rjct_duplicate_link` | Duplicate link exists |
| `rjct_not_found` | Mapping not found |
| `rjct_invalid_request` | Invalid request format |
| `rjct_server_error` | Server error |

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Server Error |

---

## Authentication

Currently, the API supports:
- No authentication (development)
- API Key (optional)
- OAuth2 (future)

---

## Rate Limiting

- Default: 100 requests per minute
- Configurable per endpoint
- Returns 429 Too Many Requests when exceeded

---

## Pagination

For list endpoints:

```bash
curl "http://localhost:8004/dfsp/providers/BANK/values?page=1&limit=10"
```

---

## Versioning

API version is specified in request header:

```json
{
  "request_header": {
    "version": "1.0.0"
  }
}
```

---

## Changelog

### Version 1.0.0 (October 2024)
- Initial release
- Link, Resolve, Update, Unlink operations
- DFSP Provider management
- G2P Connect compliance

---

**Last Updated**: October 2024
**Version**: 1.0.0

