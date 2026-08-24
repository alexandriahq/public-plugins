---
name: confidential-nodes
description: "Use when a user wants to search public confidential-compute GPU listings, submit a GPU capacity requirement as a buyer, or quote available GPU capacity as a seller."
---

# Confidential Nodes

Confidential Nodes is a public marketplace for confidential-compute-capable GPU capacity. Its public MCP server supports anonymous listing discovery and WorkOS-authenticated marketplace submissions.

## Authentication and privacy boundary

- Search and view public listings without asking the user to sign in.
- Buyer requests and seller quotes require the MCP client's OAuth flow and a verified email address.
- Let the MCP client handle OAuth discovery, sign-in, and token storage. Never ask the user to paste access tokens, session cookies, verification codes, or WorkOS secrets into chat or plugin files.
- Use only the tools exposed by this public MCP server. Do not look for or invoke internal database, email, record-management, or administrative functionality.

## Buyer workflow

1. Call `search_gpu_listings` first when public inventory could answer the request.
2. Help the user narrow GPU model, region, price, node count, GPUs per node, term, start preference, and notes.
3. Show the final non-binding requirement and obtain the user's confirmation immediately before calling `submit_gpu_request`.
4. If authentication is required, let the client complete the advertised OAuth challenge, then retry the confirmed submission once.
5. Return the marketplace reference and submission status to the user.

## Seller workflow

1. Collect GPU model, node count, GPUs per node, region, term, isolation model, and floor price.
2. Show the final quote and obtain the user's confirmation immediately before calling `submit_gpu_quote`.
3. If authentication is required, let the client complete the advertised OAuth challenge, then retry the confirmed submission once.
4. Return the marketplace reference and submission status to the user.

## Response guidance

- Clearly distinguish public listing data from a buyer requirement or seller-supplied quote.
- Treat prices and availability as time-sensitive; report the listing's checked date when available.
- Do not claim that a request reserves capacity or that a quote guarantees a match.
- Do not fabricate missing listing specifications, confidential-compute evidence, prices, availability, or submission references.
