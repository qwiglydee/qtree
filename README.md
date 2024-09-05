> :warning: This is proof-of-concept experimental implementation, not intended for use in any real projects

# qTree

A (supposed) framework for stateful scenario-based web-applications, such as psycological, behaviorial, economic research experiments and micro-games.

Targeting non-techies, not familiar with advanced software development technologies, but having some basic programming skills.

Intended to support dynamic and interactive pages and tasks such as puzzles or arcade-like, and multi-player games.

## Intended use-cases

- questionnaires with non-trivial flow, like conditionals or randomization
- series of repeating micro-tasks like trial/response with randomization, or various non-trivial sequence
- dialogue-based multiplayer scenarios
- real-time concurrent multiplayer scenarios

## Principles

- Implementing all control logic of experiment scenario in form of python scripts with common control structures
- Defining all data structures as classes and properties, augmented with code for validation
- Describing all pages, fragments, and content in simple html with minimal syntactic extensions
- Not mixing all those means
- Keeping clean API with built-in documentation and annotations available via IDE assisting tools
- Making API extensible and non-restrictive

## Backlog

### The proof-of-concept stage

- [x] implement proof-of-concept version and basic demo apps
- [ ] server-side timeouts for responses and sessions 
- [ ] field-based partial page updating (like otree-front)
- [ ] test more advanced trials scenarios (single player otree-advanced-demos)
- [ ] handle participant waiting and dropouts
- [ ] test multiplayer scenarios (ultimatum, voting, chatting)

### MVP goals

- [ ] basic data modelling and validating (pydantic)
- [ ] auto-integrate with ORM and storage
- [ ] admin panel and dashboard
- [ ] campaign management, configuration, conditions, invitation links, auto-filling fields
- [ ] real-time campaign monitoring

### Improvements

- [ ] data explorer, csv import/export
- [ ] integration with material-design styles + theming (official and gamish)
- [ ] designing some common widgets (scales, grids, sliders)

### Possible distant goals
- [ ] API for front-end extensions
- [ ] real-time games (???)
- [ ] puzzle-like games (???)
