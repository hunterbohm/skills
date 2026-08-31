# Runtime questionnaire

Before any implementation write, ask these questions in this order. Ask exactly one, wait for its answer, record it in the workflow contract, then ask the next.

1. What machine and runtime will run this?
2. Who owns the scheduler or trigger?
3. Which agent/model will perform the one bounded joint?
4. Which secret store holds the needed secret names?
5. What exact destination receives the output?
6. Who is the named approver and what gate clears consequential action?
7. Where will visible failures go?

An answer may be "none" only where the approved card makes that field unnecessary. Stop when a required answer is missing. Available tools and the current machine are not answers.
