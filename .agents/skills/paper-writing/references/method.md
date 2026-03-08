# Method

## Job

Explain:

1. what objects the method operates on
2. how the pipeline works
3. why each component exists
4. how the method differs from strong baselines

## Default Order

1. setup and notation
2. system or pipeline overview
3. core mechanism
4. training or optimization
5. complexity, implementation, or inference notes if needed

## Writing Rules

1. introduce notation only when it earns its keep
2. show the pipeline before diving into equations when the system is complex
3. isolate the key novelty in its own subsection
4. distinguish "what happens" from "why it helps"
5. when using equations, narrate them in words

## Paragraph Roles

Overview paragraph:

- define inputs, outputs, and goal
- locate the paper's main intervention

Mechanism paragraphs:

- one component per paragraph or subsection
- state responsibility and interaction with other components

Algorithm or training paragraph:

- specify objective, update rule, or search process
- mention approximations and constraints

## Common Failure Modes

1. using undefined symbols too early
2. mixing implementation trivia with core method
3. describing modules without their interaction
4. equations with no verbal interpretation

## When To Also Load

1. load `architecture-figures.md` if a framework diagram is needed
2. load `arxiv-source-workflow.md` if you want method subsection patterns from exemplars
