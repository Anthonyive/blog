---
layout: post
title:  "ER Model Study Note"
author: Yuchen Zhang
categories: computer
date: Thu, 06 May 2021 21:48:45 -0000
tags: ["study-notes", "er-model"]
---

![header comic](https://pbs.twimg.com/media/BoUn8iUIgAAq-CU.png)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [ER Model](#er-model)
  - [Basic Stuff](#basic-stuff)
    - [Entities and Attributes](#entities-and-attributes)
    - [Relationships](#relationships)
  - [Subclasses](#subclasses)
    - [Subclasses in ER Diagrams](#subclasses-in-er-diagrams)
  - [Constraints](#constraints)
    - [Modeling Constraints](#modeling-constraints)
    - [Why Constraints are Important?](#why-constraints-are-important)
    - [Keys in ER Diagrams](#keys-in-er-diagrams)
    - [Single Value Constraints (Value-based Constraints)](#single-value-constraints-value-based-constraints)
    - [Referential Integrity Constraint](#referential-integrity-constraint)
  - [Weak Entity Sets](#weak-entity-sets)
  - [Design principles](#design-principles)

## ER Model

- Gives us a language to specify
  - what information the db must hold
  - what are the relationships among components of that information
- Proposed by Peter Chen in 1976
- What we will cover
  - basic stuff
  - subclasses
  - constraints
  - weak entity sets
  - design principles

### Basic Stuff

#### Entities and Attributes

- *Entities*
  - real-world objects distinguishable from other objects
  - described using a set of attributes
- *Attributes*
  - each has an atomic domain: string, integers, reals, etc.
- *Entity set*: a collection of similar entities

#### Relationships

- Modeled as a mathematical set
- Binary and multiway relationships
- Converting a multiway one into many binary ones
- Constraints on the degree of the relationship
  - many-one, one-one, many-many
  - limitations of arrows
- Attributes of relationships
  - not necessary, but useful

### Subclasses

#### Subclasses in ER Diagrams

- Assume subclasses form a tree.
  - I.e., no multiple inheritance.
- Isa triangles indicate the subclass relationship.
  - Point to the superclass.

### Constraints

- A constraint = an assertion about the data in the database that must be true at all times
- Part of the database schema
- Very important in database design
  - To ensure data integrity

#### Modeling Constraints

Finding constraints is part of the modeling process.

Commonly used constraints:

**Keys**: social security number uniquely identifies a person.
**Single-value constraints**: a person can have only one spouse.
**Referential integrity constraints**: if you work for a company, it must exist in the database.
**Domain constraints**: peoples' ages are between 0 and 150.
**General constraints**: all others (e.g., at most 50 students can enroll in a class)

#### Why Constraints are Important?

- Give more semantics to the data
  - help us better understand it
- Allow us to refer to entities (e.g., using keys)
- Enable efficient storage
  - E.g., store ages as tiny integer (1 byte for example)
- Enable efficient lookup
  - E.g., creating an index on key

#### Keys in ER Diagrams

{% figure keys-in-er-diagrams png "Keys in ER Diagrams" %}

- Every entity set must have a key
  - Why? Because entities of an entity set need "help" to identify them uniquely.
- A key can consist of more than one attribute
- There can be more than one key for an entity set
  - one key will be designated as primary key
- Requirement for key in an isa hierarchy
  - Root entity set has all attributes needed for a key

{% figure subclasses-in-er-diagrams png "Subclasses in ER Diagrams" %}

#### Single Value Constraints (Value-based Constraints)

- An entity has at most one value for a given attribute or relationship
- An attribute of an entity set has a single value or NULL
  - i.e., the value may be missing
- A many-one relationship also implies a single value constraint

#### Referential Integrity Constraint

- *Referential Integrity constraint*: exactly one value exists in a given role
- An attribute has a non-null, single value
  - this can be considered a kind of ref. int. constraint
- However, we more commonly use such constraints to refer to relationships
- In some formalisms we may refer to other object but get garbage instead
  - e.g. a dangling pointer in C/C++
- The Referential Integrity Constraint on relationships explicitly requires a reference to exist

{% figure referential-integrity-constraints png "Referential Integrity Constraint Example" %}

### Weak Entity Sets

Entity sets are *weak* when (some or all of) their key attributes come from other entity sets to which they are related.

This happens when:

- part-of relationships
- splitting n-ary relationships to binary.

{% figure weak-entity-sets png "Weak Entity Sets Example" %}

### Design principles

- be faithful
- avoid redundancy
- KISS