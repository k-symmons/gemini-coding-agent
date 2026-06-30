# Bug: `gemini-2.5-flash-lite` intermittently returns empty STOP response after function call

**Repo:** googleapis/python-genai

## Description

`gemini-2.5-flash-lite` intermittently returns an empty `STOP` response — `content.parts=None`, `response.text=None`, `candidates_token_count=None` — on the turn after function call results are sent back. When this happens consistently across iterations it causes agents to loop until they exhaust their iteration limit. `gemini-2.5-flash` does not exhibit this behaviour.

## Reproduction

In a multi-turn agent loop using `generate_content` with a `system_instruction` and several registered tools, the second turn (after returning function results) consistently returns an empty response:

```
Prompt tokens: 576
Response tokens: None        # candidates_token_count is None
finish_reason: STOP
content.parts: None
response.text: None
```

The failure reproduced 100% of the time in the full agent context but not reliably in minimal isolation tests, suggesting it is sensitive to the combination of system instruction, tool count, and accumulated message history.

## Confirmed workaround

Switching `model` from `gemini-2.5-flash-lite` to `gemini-2.5-flash` resolves the issue completely.

## Environment

- `google-genai` version: 1.12.1
- Python: 3.13
- Failing model: `gemini-2.5-flash-lite`
- Working model: `gemini-2.5-flash`

## Related

- https://github.com/block/goose/issues/6293
- https://github.com/BerriAI/litellm/issues/24442
- https://github.com/langchain-ai/langchainjs/issues/8589
