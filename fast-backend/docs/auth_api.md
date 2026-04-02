# API Documentation: Authentication

This section covers the authentication APIs, including user registration (signup) and session-based login.

## 1. User Signup

**Endpoint**: `POST /api/v1/auth/signup`

### Description
Creates a new user account. Validates that the email is unique and that the password matches the confirmation password.

### Request Body
- `email` (string, required): The user's email address (used as the username).
- `full_name` (string, required): The user's full name.
- `password` (string, required): The user's password.
- `confirm_pass` (string, required): Password confirmation (must match `password`).
- `role` (string, optional): The user's role (e.g., "Physician", "Admin").
- `organization` (string, optional): The user's organization or hospital name.

### Sample CURL Request
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword123",
  "confirm_pass": "securepassword123",
  "role": "Physician",
  "organization": "St. Marys Hospital"
}'
```

### Success Response (200 OK)
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "Physician",
  "organization": "St. Marys Hospital",
  "id": 1
}
```

---

## 2. User Login

**Endpoint**: `POST /api/v1/auth/login`

### Description
Authenticates the user using email and password. If successful, returns a session-backed access token valid for 24 hours.

### Request Body
- `email` (string, required): The user's registered email.
- `password` (string, required): The user's password.
- `full_name` (string, optional): Not used for authentication but required by the simplified schema.
- `confirm_pass` (string, optional): Not used for authentication but required by the simplified schema.

### Sample CURL Request
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "confirm_pass": "securepassword123"
}'
```

### Success Response (200 OK)
```json
{
  "access_token": "RxXGsjMbauqYpvVEe6ELA81m2eT3OpFpNUa3dkgp",
  "token_type": "bearer"
}
```

> [!NOTE]
> The `access_token` should be included in the `Authorization` header as a Bearer token for protected requests: `Authorization: Bearer <access_token>`.

---

## 3. Get Current User Profile

**Endpoint**: `GET /api/v1/auth/me`

### Description
Returns the profile of the currently logged-in user. Requires a valid Bearer token.

### Headers
- `Authorization: Bearer <access_token>` (required)

### Sample CURL Request
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/auth/me' \
  -H 'Authorization: Bearer <access_token>'
```

### Success Response (200 OK)
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "Physician",
  "organization": "St. Marys Hospital",
  "id": 1
}
```
