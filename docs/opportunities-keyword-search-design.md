# Opportunities Keyword Search Design

## Phase

7.1.18.1 Keyword Search

## Objective

Allow users to quickly find opportunities using free-text search.

## Scope

Frontend only.

No backend changes.

No API changes.

No database changes.

## Search Fields

The keyword search must match:

- Job title
- Company name
- Location
- Description

## Search Rules

Case insensitive.

Partial match supported.

Examples:

"python"
→ Python Developer
→ descriptions containing Python

"paris"
→ opportunities located in Paris

"amazon"
→ opportunities at Amazon

## UX

Location:
Above the opportunities list.

Placeholder:

Search opportunities...

## Empty State

No opportunities match your search.

## Out Of Scope

- Boolean search
- Regex
- Advanced filters
- Saved searches
- Highlighting
- Backend search

These items belong to future phases.
