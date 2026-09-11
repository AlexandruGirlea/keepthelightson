# Keep the model replaceable

Design guidance for moving a capability from one hosted model to another, or to a model you
run yourself, as a configuration change rather than a rewrite. It exists because the events
that end access are commercial and political, and they arrive with days of notice: a
deprecation, a price rise, a policy change, an export control, an acquisition. A replaceable
model shortens the switch. It is not a manual path: under clause 4.2.4 a second hosted supplier
does not lift a capability above L1 until common-mode failure has been assessed and recorded,
and it does nothing for the day no supplier will do. Build both.

## The shape

```text
capability interface   classify(claim) -> Category
        |
   one adapter         prompt, tools, parsing, retries, logging, the off switch
        |
   provider clients    OpenAI-compatible, Anthropic, Google, Mistral, a self-run server
```

- Name the capability in business terms and give it one interface. The model is one
  implementation of it, the human path is another (specification, clause 4.2).
- One adapter per capability, or one shared adapter, is the only code that knows which
  provider is in use. Nothing else imports a provider SDK.
- The provider and the model are chosen by configuration per capability, with a key per
  provider, so that a switch is a deployment setting and not a pull request. The same setting
  is how a drill cuts the model (clause 4.4.2) and how the off switch is enforced.
- Log the request, the model identifier and the response version with every call so you can
  compare results later.

## What does not travel

These choices make switching providers harder. Decide which trade-offs you can accept.

- Prompts written against one model's quirks. Keep the system prompt and the messages in your
  own neutral structure and translate in the adapter; keep the rules the prompt relies on
  written down outside it (clause 4.6.2).
- Tool and function definitions. Hold them as JSON Schema in your own format and translate per
  provider; the calling conventions differ. Validate structured output yourself instead of
  relying on one provider's mode.
- Embeddings. Vectors from one model cannot be mixed with another's. Store the source text and
  the embedding model identifier with every vector, keep a re-indexing job that works, and
  budget for re-embedding the whole corpus when the model is retired.
- Fine-tunes, hosted assistants, hosted retrieval and provider-side state. The weights and the
  state stay with the provider. Keep the training data and an evaluation set; prefer prompting
  and your own retrieval where a switch matters.
- Provider-only features (extended context, caching modes, built-in search, safety settings).
  Use them behind the adapter with a documented behaviour for providers that lack them.

## Prove the switch before you need it

- Keep an evaluation set of real inputs with accepted outputs for each capability, drawn from
  the persisted inputs and decisions (clause 4.6.1).
- Run it against the alternative provider, or the self-run model, on a schedule, and record
  quality, refusals, latency, cost and context limits. A documented switch remains unproven
  until you run it.
- Record the result in the register entry: whether the switch is a configuration change, a
  code change, or does not exist.

## Libraries, and their limits

Many providers and self-run servers support an OpenAI-compatible endpoint. LiteLLM (a proxy
and SDK across providers), the Vercel AI SDK (TypeScript), Spring AI (Java), Semantic Kernel
(.NET and Python), and LangChain or LlamaIndex (broad and heavy) each give one place to change
the provider. An internal gateway does the same and is also where logging, budgets and the
off switch can live. These tools still need to handle the provider differences above, including
tool calling, structured output and embeddings. They give you one place to make a change; you
still need to test that change.
