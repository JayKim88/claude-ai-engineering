# Test Project Specification

> **Version**: 1.0.0
> **Date**: 2026-02-13
> **Status**: Implementation in progress

---

## 1. Overview

A simple user authentication system with JWT tokens and email verification.

---

## 2. Functional Requirements

### FR-1: User Registration
**Priority**: High
Users must be able to register with email and password. System validates email format and password strength (min 8 chars, 1 uppercase, 1 number).

### FR-2: Email Verification
**Priority**: High
After registration, system sends verification email. Users must verify email before login.

### FR-3: User Login
**Priority**: High
Users can login with verified email and password. System returns JWT token valid for 24 hours.

### FR-4: Password Reset
**Priority**: Medium
Users can request password reset via email. Reset link expires after 1 hour.

### FR-5: Profile Management
**Priority**: Low
Users can view and update their profile information (name, bio, avatar).

---

## 3. Non-Functional Requirements

### NFR-1: Security
All passwords must be hashed with bcrypt (cost factor 10). JWT tokens use HS256 algorithm.

### NFR-2: Performance
User registration must complete within 2 seconds. Login within 1 second.

### NFR-3: Scalability
System must support 10,000 concurrent users.

---

## 4. Technical Design

### 4.1 Data Models

#### User Model
- id: UUID (primary key)
- email: String (unique, indexed)
- password_hash: String
- name: String
- bio: Text (optional)
- avatar_url: String (optional)
- email_verified: Boolean (default: false)
- created_at: Timestamp
- updated_at: Timestamp

#### VerificationToken Model
- token: UUID (primary key)
- user_id: UUID (foreign key)
- token_type: Enum (EMAIL_VERIFY, PASSWORD_RESET)
- expires_at: Timestamp
- used_at: Timestamp (nullable)

---

## 5. API Design

### POST /api/auth/register
Creates new user account. Returns 201 on success.

### POST /api/auth/verify-email
Verifies email with token. Returns 200 on success.

### POST /api/auth/login
Authenticates user. Returns JWT token.

### POST /api/auth/forgot-password
Initiates password reset. Sends reset email.

### GET /api/users/profile
Returns current user profile. Requires authentication.

### PUT /api/users/profile
Updates user profile. Requires authentication.

---

## 6. Edge Cases

### EC-1: Duplicate Email Registration
If user tries to register with existing email, return 400 error with clear message.

### EC-2: Expired Verification Token
If verification token expired, allow user to request new token.

### EC-3: Too Many Failed Logins
After 5 failed login attempts, lock account for 15 minutes.

### EC-4: Invalid JWT Token
Return 401 error with "Invalid or expired token" message.

---

## 7. Testing Requirements

- Unit tests for all models and services
- Integration tests for API endpoints
- E2E tests for registration → verification → login flow
- Security tests for password hashing and JWT validation
