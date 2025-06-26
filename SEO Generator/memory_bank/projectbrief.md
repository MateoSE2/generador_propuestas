# Project Brief: SEO Product Description Platform

## Overview

**SaaS platform** that generates **AI-powered SEO-optimized product descriptions** for e-commerce catalogs. Multi-tenant architecture from day one, designed for commercialization to serve multiple independent clients.

## Core Value Proposition

The platform allows users to ingest product data, generate optimized content using LLMs, and sync this content back to their stores with contextual enrichment from internet searches.

## Supported Ingestion Modes

- **Excel Uploads** (.xlsx format)
- **Direct integration with WordPress + WooCommerce** (bidirectional sync)

## Core Functional Scope

### 1. Configuration Screen

- Manage and edit prompt templates per tenant
- Modify generation parameters (model, temperature, max tokens, etc.)
- Support for multiple preset templates
- Set global or per-tenant defaults for language, brand tone, SEO focus

### 2. Executions Screen

- View all generation jobs
- Trigger new jobs via Excel upload or WooCommerce sync
- Monitor progress and status of each job
- Filter by source, date, status, language, etc.
- Options for:
  - Re-run individual generations
  - Sync results back to WooCommerce
  - Reset generation state

### 3. Execution Detail Screen

- Detailed breakdown of each job
- View original product input and generated description
- Manual editing (if enabled)
- Buttons to:
  - Resend description to WooCommerce
  - Retry failed generations
  - Export or copy outputs

## Technical Features

### Multitenancy

- Each tenant has isolated configurations, executions, and integrations
- Shared infrastructure with tenant-based access control
- Tenant-specific tokens, credentials, and limits
- Admin-level dashboards to monitor global usage

### LLM-Based Generation

- Prompt templates with dynamic variables (e.g. `{{title}}`, `{{category}}`)
- Backend supports multiple providers (OpenAI, Anthropic, Local)
- Flexible model selection per tenant or per execution

### Internet-Based Contextual Enrichment

- For each product, the system performs an **internet search** to retrieve contextual data (specs, descriptions, reviews)
- Injects this data into the prompt to improve quality of output
- Configurable filters, trusted domains, and rate-limits
- Results are cached per product to reduce redundant lookups

### Parallel Job Execution

- Batch jobs are distributed across worker pools
- Asynchronous queueing system (Celery + Redis or equivalent)
- Auto-scaling and timeouts for long-running generations
- Retry and error logging mechanisms

## Integration: WooCommerce (Bidirectional)

### Pull Operations

- Read product data via WooCommerce REST API or direct DB connection
- Retrieve product name, categories, attributes, current description
- Map fields dynamically to prompt input

### Push Operations

- After generation, write back the new SEO description to WooCommerce
- Support for:
  - **Manual sync per item or batch**
  - **Auto-sync after generation (configurable)**
  - **Reset and re-sync description manually**

### Sync Control UI

- Button: "Resend to WooCommerce"
- Button: "Reset Description"
- Button: "Retry Generation"
- Visual indicator of sync status (pending, synced, error)

### Authentication & Security

- Each tenant stores their own WooCommerce credentials securely
- Optional OAuth flow or API key + store URL
- Audit logs for sync operations

## Excel Integration

- Upload Excel files (.xlsx) with product data
- Map columns to expected prompt inputs
- Launch generation in batch mode
- Download results with original input + generated output
- Option to push back to WooCommerce for matching SKUs

## Project Goals

- **Primary**: Create a commercializable multi-tenant SaaS platform
- **Secondary**: Demonstrate scalable AI integration with e-commerce
- **Tertiary**: Establish patterns for similar B2B SaaS products

## Success Metrics

- Multi-tenant architecture functioning correctly
- Successful WooCommerce bidirectional sync
- Quality SEO content generation with internet enrichment
- Scalable job execution system
- User-friendly configuration and monitoring interfaces
