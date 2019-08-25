---
layout: default
title: Useful Checklists
---

These are fairly small lists that I want to read every once in a while.

## Releasing Software for Humans

- Design from the user perspective
- Don't advertise until close to finishing
- Timing is important. Don't announce something cool when there's something else going on
- Include usage example in README.md
- Test on all platforms users use
- Include call for feedback in `--help`, and solicit users to use it
- You only get one first impression
- Separate user docs from developer docs
- Manually run through the full setup and some common scenarios before you demo.

## What To Put in Function Documentation

I love this [section](https://cloud.google.com/apis/design/documentation#checklist) of Google's API design book.

### Checklist for all descriptions

Make sure each description is brief but complete and can be understood by users
who don't have additional information about the API. In most cases, there's
more to say than just restating the obvious; for example, the description of
the `series.insert` method shouldn't just say "Inserts a series." — while your
naming should be informative, most readers are reading your descriptions
because they want more information than the names themselves provide. If you're
not sure what else to say in a description, try answering all of the following
questions that are relevant:

- What is it?
- What does it do if it succeeds? What does it do if it fails? What can cause it to fail, and how?
- Is it idempotent?
- What are the units? (Examples: meters, degrees, pixels.)
- What range of values does it accept? Is the range inclusive or exclusive?
- What are the side effects?
- How do you use it?
- What are common errors that may break it?
- Is it always present? (For example: "Container for voting information. Present only when voting information is recorded.")
- Does it have a default setting?

## Sayings I Like

These are from various places and may be misremembered.

- Your work shapes your tools and your tools shape your work
- There that scattereth and yet increaseth
- The worker is worthy of his wages.
