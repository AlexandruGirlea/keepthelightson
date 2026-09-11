# What counts as a dependency

Grade business capabilities that normally require an AI system supplied and operated by
another party (specification 1.1 and section 2). Review human control under principle 6 for
both hosted and self-run runtime AI, without adding supplier-dependence gates.

## First decide what the repository is

| Repository | Treatment |
|---|---|
| Product or service: application, API, worker, pipeline or internal business tool | Assess its business capabilities. |
| Library, SDK, client, framework, plugin or template | No level. Report the suppliers it wraps and whether applications can substitute or omit them. |
| Demo, sample, notebook, course or documentation | No level. Describe its scope and stop. |
| Monorepo | Assess each product; trace shared libraries as that product's internals. |

Use README/package purpose, entry points and deployment configuration to support the
classification. Registry packaging with `main`/`exports` and no server suggests a library;
a server/worker, deployment, database or operating interface suggests a product. If unclear,
state the uncertainty and inspect the runtime code.

## In scope

Include hosted chat, completion, embedding, speech, vision, image and video APIs; hosted
fine-tunes, agents and managed retrieval; and SaaS features that cannot deliver their result
without a hosted model. The provider controls the running system, access terms and prices.

Trace gateways, proxies, SDKs and orchestration frameworks through configuration to the actual
supplier. A company gateway or bring-your-own-key interface does not remove dependence.

## Out of scope

Record these in the inventory without numbered gates or levels:

- Models the implementer runs from its own or held weights, including traditional ML,
  classifiers, Ollama, llama.cpp and vLLM. Rented compute is a cloud dependency. Note restrictive
  weights licences separately.
- Development-only AI, such as coding assistants and review steps in CI.
- Samples, tests and provider SDKs with no call on a business runtime path.

Self-run runtime AI still receives a principle 6 control review. Development-only, unused and
sample AI does not.

## Provider coupling, reported and not gated

For each hosted capability, record how tightly the code is tied to its provider and what
would need to change to replace it. Portability does not affect the KLOD level. Code locations
alone do not establish migration time; report timing only when supported by an observed switch.

- Where the provider is named: one adapter or gateway, or SDK calls at many sites.
- Whether the provider and model are chosen by configuration or hard-coded.
- Provider-specific features in use: tool-calling formats, structured-output modes, hosted
  assistants or retrieval, fine-tunes, caching modes.
- Embeddings stored without the embedding model identifier, and whether re-indexing exists.
- Evidence that a switch has ever been run: an evaluation set, a recorded comparison.

Rate each capability **one place to change**, **several places** or **everywhere**, with the
file evidence, in the report's Portability section.

## Judgement calls

- **Hosted normal path, local fallback:** the capability remains supplier-dependent. Assess
  the proposed fallback against the manual-path gates: instructions, people, limits and, for
  higher levels, drills with hosted AI cut, measurements and demonstrated performance. A switch
  to a local model alone does not establish human capability.
- **Self-run normal path, optional hosted model:** no supplier-dependence level when hosted
  use is experimental, optional or development-only. Record that hosted use in the inventory.
- **Bring your own key:** assess the default or documented hosted configuration and state that
  the supplier is selected per deployment.
- **Embeddings:** trace indexing and corpus refresh as well as query answering. A hosted
  embedding dependency can stop re-embedding even when another path still answers queries.
