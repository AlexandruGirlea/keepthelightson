# Keep people in control

Give authorised people a way to stop AI actions and take over without the model's help.
They need it when a supplier becomes unavailable or a model acts unsafely, including after malicious
instructions, poisoned inputs or a compromised model.

This sixth KLOD principle applies to AI running in your application, whether you use a hosted
model or run it yourself. It is design guidance, separate from the
[specification's supplier-dependence clauses and L0 to L3 levels](https://keepthelightson.eu/standard.html).

## Enforce control where actions happen

- **Provide an AI-off control and show the current mode.** Switching AI off must work without provider approval.
  The model cannot authorise its own restart.
- **Enforce the mode outside the model.** Check the mode where the server, worker or device
  accepts actions. Stopping new model requests leaves queued calls active unless the server,
  worker or device rejects them. Keep the selected mode across restarts and define a safe response
  if the system cannot read it.
- **Account for work already under way.** Reject late results and queued AI commands after AI
  is switched off. Record which actions have completed, which were cancelled and which have an
  unknown outcome before anyone retries. Some effects cannot be undone.
- **Keep manual work usable.** People need the current inputs, work status, permissions and
  controls. Check that validation, data retrieval and task execution still work without AI.
  Keep authentication and access restrictions in place.
- **Require deliberate restart.** Record who switched modes and why. Require authorised human
  approval to resume. The supplier coming back online must not restart AI automatically.
  Check the status of pending work and prevent duplicates when switching in either direction.

A helpdesk, for example, rejects late AI replies while staff read tickets and send manual
replies. An IoT service must also block old AI commands in its workers and device gateway.

## Physical equipment

For IoT, medical robots, nuclear facilities and government or military systems, removing AI
authority does not necessarily mean cutting power. Keep independent safety systems, interlocks
and essential non-AI controls. Switching off AI in an application serves a different purpose
from a physical emergency stop.

The responsible specialists must decide what happens next: trained human operation, restricted
operation, safe hold or controlled shutdown. Name the operators, list the information they need
and set the required response time. A person who lacks the training or time to act safely cannot
serve as the backup.

Follow established safety, authorisation and engineering-validation procedures. Medical
procedures, plant setpoints and operational military controls must come from the responsible
specialists.

## Verify takeover

In isolated tests or simulation, stop AI during an active request. Check that late results and
queued commands are rejected, people can use the manual controls, and AI resumes only with
human approval. Test denied requests, process restarts and failures to read the stored control
mode. Check that each produces the agreed safe response.

These implementation checks do not show how much work people can sustain and do not count as
real-work L2 drills.

## Repository evidence

Follow the off switch through background jobs and late results to the code or device that accepts
actions. Cite the code, tests and operating records, and identify any missing deployment or
hardware evidence. A flag alone does not prove that the switch works.

Report gaps as **human-control observations**. For each one, explain what could go wrong,
provide the evidence, name an owner and give the next action. Keep them separate from findings
against the numbered clauses. A repository review cannot certify equipment safety or detect
backdoors in model weights. Suspicious output alone is not proof of a backdoor.

## Sources

- [NIST AI RMF, MANAGE 2.4 and GOVERN 1.7](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/):
  responsibility for overriding, deactivating and safely decommissioning AI.
- [NIST SP 800-82r3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf):
  independent safety systems and equipment-specific safe states.
- [Sleeper Agents research](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training):
  constructed backdoors that survived tested safety training, not evidence about a deployed provider.
