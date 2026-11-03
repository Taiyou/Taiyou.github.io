---
title: The Shadow Clone Problem: Governance for BMIs and AI Agents · Hiro Taiyo Hamada
description: BMIs widen what we can express and AI agents widen what we can do. The bottleneck that remains is the return — what comes back to one mind — and its two costs, integration bandwidth and provenance, have to be governed.
label: Blog · 3 November 2026
heading: The Shadow Clone Problem: Governance for BMIs and AI Agents
lead: Brain–machine interfaces widen what we can express. AI agents widen what we can do. What neither widens is the return — how much one mind can take back in, and how much of its lineage it can keep.
date: 2026-11-03
original: https://note.com/hirotaiyohamada/n/n003b60d63692
toc: true
---
<p class="post-origin">This essay expands <a href="https://note.com/hirotaiyohamada/n/n003b60d63692" target="_blank" rel="noopener">a Japanese essay on note</a> (13 September 2026). It draws on an ongoing project, Dividual Clones (kagebunshin), on memory and provenance in multi-agent systems.</p>

## Introduction: the limit is not making clones

In the manga Naruto, the shadow clone technique (影分身, kage bunshin) creates copies of the user that act independently. When a clone is dispelled, what it experienced flows back into the original. The catch, well known to fans, is that the fatigue flows back too: dispel too many clones at once and the original is overwhelmed. The limit of the technique is not making clones. It is taking them back in.

This is a fair picture of where human–AI collaboration is heading. People want two things from AI. The first is to **draw out the information inside themselves more richly**. The second is to **run more work in parallel than they could ever handle alone**. The decoding technology that serves the first need is the **brain–machine interface (BMI)**; what serves the second is the **AI agent**.

The two are almost never drawn in the same picture. BMIs are discussed in neural engineering and clinical medicine; agents in software development and multi-agent research. I have been arguing that BMIs on their own solve only half the problem, and that the two should be designed together. Seen from the human side, they are attacking the same problem from opposite ends — and together they run straight into the problem of the shadow clone.

A clone has a life in three moments. It is **sent out** with an intent, it **acts** on its own, and it **comes back**. Each moment has its own bandwidth limit, and each needs its own kind of governance.

## Sending out: the bandwidth of expression

Humans have bandwidth limits. When we type on a keyboard or give instructions by voice, we get only a tiny fraction of what is in our heads out into the world — our judgments, where our attention is pointed, intentions that have not yet become words. Keyboards and voice are discrete, explicit, and slow. We first translate what we want to convey into words, and only then type it in. A great deal is lost in that translation.

This is a limit on the input side: the **bandwidth of expression**.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig1.svg" alt="Two channels lead out of a person's inner state. Keyboard and voice form a narrow, slow channel that yields only a few words; a BMI forms a wide channel that yields rich intent." loading="lazy"><figcaption>Figure 1. BMIs and the bandwidth of expression</figcaption></figure>

What a BMI tries to capture is the continuous, implicit state that exists before that translation: where attention is pointed, what feels off, whether we are hesitating or sure. The real strength of a BMI lies in **extracting rich intent with as little loss of information as possible**.

One can imagine using a BMI to steer agents directly. But the job of the BMI is to make the human side's intent denser — to decide well what each clone is sent out with. Parallelizing and organizing what comes after belongs to a separate layer.

## Acting: the bandwidth of action

However clear our intentions are, each of us has only one body and one stream of time. We cannot push ten jobs forward at once. This is a limit on the output side: the **bandwidth of action**.

Agents widen it. As of 2026, it is fair to say that in most cases agents already exceed the abilities of the average person. They write code, do research, and produce documents, and dozens of them can take one person's intent and carry out separate pieces of work at the same time.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig2.svg" alt="One person's rich intent passes through a harness made of access, memory and reporting governance, then branches out to N agents working in parallel on code, research and documents." loading="lazy"><figcaption>Figure 2. The harness: one intent, N agents</figcaption></figure>

Multi-agent coordination is not easy, however. Human organizations have mechanisms for keeping many people pointed at one goal: work rules, approval authority, records, reporting lines. Agents need the same thing. This is what is called a **harness**, and I think it needs three mechanisms — one for each moment of the clone's life.

The first belongs here, at the moment of acting:

- **Access governance** — who may access what, and who may decide what.

The other two belong to the return, and are introduced below.

## Coming back: the bandwidth of reception

Each agent that branches off builds up its own context. Eventually it finishes its work, and that experience flows back to the human. Here the two demands collide. BMIs have made intent richer, and rich intent produces rich results. Agents have made processing parallel, and parallel processing produces many results. All of it **floods into the receiving bandwidth of a single person**.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig3.svg" alt="Results from many agents, each carrying its own context, converge into a funnel that summarizes and abstracts them before a narrow outlet reaches one person." loading="lazy"><figcaption>Figure 3. The bandwidth of reception</figcaption></figure>

The more we widen the input and output sides, the narrower a person's **bandwidth of reception** becomes in relative terms. This is not a technical shortcoming. Human behavior appears to run at roughly 10 bits per second, while our senses take in on the order of a billion ([Zheng & Meister](https://arxiv.org/abs/2408.10234v2)). If that rate reflects thinking itself rather than our fingers and voices, then a wider pipe into the brain does not make the brain take in more. The third bandwidth follows from the structure, not from immature technology.

This holds even in the most ambitious futures. In his manifesto [Phase Lock](https://phaselock.satpugnet.com/), Saturnin Pugnet suggests that accelerated whole-brain emulations of a person could supervise an AI at machine speed and then report back at a pace the person can follow. That is a shadow clone in the most literal sense — and it ends with the same step as every agent pipeline: "report back." That step is usually written in a single sentence. It is where the cost lives.

## The two costs of the return

The return has two separate costs.

- **Integration bandwidth (B)** — how much of what a clone lived through can be folded back into the one who acts and decides. For a person, it is bounded by attention and central processing; for an agent, by the context window of whoever does the merging.
- **Provenance (C)** — the cost of keeping track of where each piece came from: which clone did it, under what instruction, from which source, and why it turned out that way. This is the cost of storing that record, verifying it, and reading it.

These costs are not independent. Provenance is itself information that has to be integrated. Every line of "who did what and why" that comes back competes for the same narrow channel as the result it describes. Whether we integrate what comes back, and whether we keep its provenance, gives four regimes (Figure 4).

<figure class="post-fig"><img src="{{root}}assets/img/blog/shadow-clone-2x2.svg" alt="A two-by-two grid. Horizontal axis: whether results are integrated into the one who acts. Vertical axis: whether provenance is kept. Dissociation: neither. Inaccessible memory: provenance kept but not integrated. Source amnesia: integrated without provenance. Accountable memory: both." loading="lazy"><figcaption>Figure 4. Four memory regimes for what comes back</figcaption></figure>

- **Dissociation** — nothing is integrated and nothing is traced. Work happened, but no one holds it and no one can say who did it.
- **Inaccessible memory** — every log is kept, but nobody reads it. The archive is complete and has no reader.
- **Source amnesia** — the conclusion is absorbed, but where it came from is lost. You know what you believe and not why, or whose belief it originally was.
- **Accountable memory** — the result is integrated and its lineage is kept, so you can both act on it and answer for it.

Today's agent stacks mostly sit in source amnesia, running at machine speed: a summary arrives without its lineage, and we act on it. Accountable memory is the corner we want, and it is the expensive one, because it asks us to pay B and C at once.

Not every piece of work needs to be there. A routine lookup can come back as a bare result; a decision someone will have to defend later cannot. This gives the second mechanism of the harness:

- **Reporting governance** — for each kind of work, choosing deliberately where its return sits among the four regimes: what is summarized and abstracted, what comes back with its lineage intact, and in what form it reaches the human.

## Layer 1 and layer 2: the trade-off, priced

Blockchains have already run into this problem, and put a price on it.

A blockchain's main chain, layer 1, is the single mind of the story. Its block space is scarce, and everything that is to count has to settle there. That is integration bandwidth. To get more done, layer-2 rollups execute transactions off the main chain — clones at work — and post their results back to layer 1. To let anyone check or challenge those results, a rollup must also publish the underlying data. This data availability is the main running cost of a rollup. It is provenance, with a market price.

The four regimes have direct counterparts:

- **Dissociation** — activity that happens off-chain and is never settled. As far as the main chain is concerned, it did not happen.
- **Source amnesia** — a chain that posts only its resulting state and keeps the data elsewhere, as validium-style designs and many sidechains do. The main chain accepts the result on the operator's word.
- **Inaccessible memory** — a rollup that publishes its data but that no one watches. Optimistic rollups are secure only if at least one honest party is reading and ready to raise a challenge; a complete record with no reader protects no one.
- **Accountable memory** — a rollup whose data sits on layer 1 and whose results are actually checked.

Rollups also offer two strategies for the return, and both translate. An optimistic rollup is accepted by default and can be challenged during a fixed window, typically about seven days — like accepting an agent's summary while keeping the right to audit it for a set period. A validity (zero-knowledge) rollup attaches a proof, so the main chain can confirm the result without reading its history at all. Validity proofs do not just choose a point between B and C; they move the frontier, making accountability cheap to verify.

Two lessons carry over with warnings. First, many rollups still depend on a single sequencer that orders all transactions. The clones are many, but the one who decides the order of their return is one — the same concentration risk an orchestrating agent poses. Second, the analogy breaks exactly where it matters. A blockchain verifies a deterministic state transition mechanically. A person cannot check a proof by intuition, and the work agents do involves meaning and judgment that do not compress into a proof. The human side of the return needs institutions and not only cryptography.

## Forgetting as a governed act

If we cannot afford to keep everything and read everything, something has to be let go. The question is whether that happens by accident or by decision.

Archival science has dealt with this for a long time. Archivists **appraise** records when they are created, deciding what is worth keeping. They set **retention schedules** that say how long each kind of record is kept, and they carry out **scheduled disposal** when that time is up. Forgetting becomes an act someone is responsible for, rather than a failure that happens to us.

Brought into a multi-agent system, this does more than pick a point between B and C. A record that will be disposed of on a known schedule does not have to be read now; what remains stays small enough to be read. Disposal, done on purpose, is what keeps provenance affordable.

Rollups again offer a working example. Since Ethereum's EIP-4844, rollup data is carried in "blobs" that nodes keep for 4,096 epochs, roughly 18 days, and then delete — long enough to cover the seven-day challenge window with room to spare. That is a retention schedule tied to the period in which the record can still be needed, followed by scheduled disposal. The chain stays light enough to run because it forgets on purpose.

This gives the third mechanism of the harness:

- **Memory governance** — what is kept, what is discarded and when, and who inherits that memory.

## Whose clone is it?

There is one more layer. In Japanese, bunshin (分身, a divided body, a clone) and bunjin (分人, the "dividual" — Hirano Keiichiro's term for the many selves a person is across their relationships) share the same first character, 分: to divide. Anthropology has a parallel line of thought in Marilyn Strathern's dividual person, made up of relations rather than sealed inside a single body.

If clones are parts of a self rather than tools held by one, provenance changes meaning. It stops being external bookkeeping and becomes part of the upkeep of a self: knowing which of my clones did this, and on what basis, is part of knowing what I did. Accountability then attaches not only to the person at the top but to the line that runs from each clone back to them.

For LLM agents, this can sound like a metaphor. For the brain emulations Pugnet describes, it is not. An emulation of you that has spent a thousand subjective hours supervising a machine comes back with experience that is yours and that you did not live. How much of it you take in, and how much of its lineage you keep, decides what kind of person you are afterward.

## The privacy of the return

So far, provenance has been a cost of storing, verifying and reading a record. With BMIs in the loop, it has a fourth component: exposure.

When intent is decoded from the brain, "which instruction did this clone act on" points back to a reading of someone's mind. The more lineage we keep, the more accountable the return — and the more there is to leak. Accountable memory, the corner we want, is also the corner with the most to lose. Provenance needs a third dimension next to integration and retention: who may see it.

Several of the ideas above turn out to be privacy measures as well.

- **The division of labor is a privacy boundary.** If the BMI layer hands on intent rather than raw signals, the boundary that keeps each clone's instructions dense also keeps the raw mind at home. Pugnet makes the same recommendation: process locally, and transmit intent rather than brainwaves.
- **Forgetting for bandwidth and forgetting for privacy coincide.** Neural recordings grow more revealing as decoders improve; a trace that shows only focus today may tell a better model of the future much more. Pugnet's answer is consent that expires unless it is renewed. A retention schedule is the same instrument. A record that has been disposed of cannot be re-read by tomorrow's model.
- **Inaccessible memory is the worst corner for privacy.** Logs that nobody reads still exist. They can be breached, demanded, and re-analyzed. They carry the full cost of exposure and none of the benefit of understanding.
- **Proving without showing.** Validity proofs let a chain confirm a result without reading its history; zero-knowledge proofs let it do so without seeing the data at all. The same move could let a clone show that it acted within its authority without revealing what it saw. One tool addresses bandwidth and privacy together — though, as before, only for what can be stated precisely enough to prove.

There is also a case for not integrating at all. Helen Nissenbaum's idea of contextual integrity holds that information appropriate in one context becomes a violation when it flows into another; access governance is that idea applied to clones. The dividual view adds that we are different persons in different relationships. Clones that act inside different relationships carry contexts that should not all be merged into a single self. Sometimes the right regime for a clone's memory is to keep it, under seal, in its own context, unintegrated on purpose. Inaccessible memory, chosen deliberately and governed, becomes compartmentalization.

## From one mind to one place: local AI

The same frame scales up. Replace the single person with a community, and the clones with local AI systems, and the shadow clone problem reappears at the scale of places.

Imagine a region that gathers what its environment says about itself — environmental DNA from water and soil, sensors on trees, records from farmers and local government — into an AI that runs locally and returns what it learns to the people who live there. Now imagine many such regions, each with its own local AI, connected into a network. Each local AI builds up its own context, as a clone does. Connecting them is a return: what each place has learned flows into a shared layer that, like layer 1, has limited room. Which of it goes up, and with how much provenance, is the design question.

Provenance here is not only accountability; it is how value finds its way home. Returning benefit to a community requires knowing which data came from where, from whose land, and which knowledge from whom. Source amnesia at this scale has a familiar name: extraction. Data flows to a center, its origin is lost, and the value it creates never returns. This is precisely the problem behind current debates on digital sequence information under the Convention on Biological Diversity, where genetic data detached from its source can generate value with no path back. Environmental DNA sits squarely inside that problem.

Each kind of data can be given a deliberate place among the four regimes:

- **Raw sensor streams and sequencing reads** stay in the place where they were collected, under a retention schedule. They are large, and like neural recordings they may reveal more to future models than anyone intended.
- **Summaries such as which species are present** are integrated into the network with their provenance intact. They make comparison across places possible and are the basis for returning value.
- **The locations of rare species** are compartmented on purpose. Keeping them out of the network is itself an act of conservation, since that information also serves poachers.
- **Local and traditional knowledge** is integrated only under explicit consent and benefit-sharing terms, so that whose knowledge it is never gets lost.

The rest of the harness carries over too. Access governance lives at the interface through which outside agents reach a local AI's tools and data — for example, servers exposed through the Model Context Protocol (MCP), an open standard for connecting AI applications to external tools and data — where the scope of what each caller may read and decide can be set. Reporting governance decides what a place returns to a question from outside, and in what form. And the warning from rollups applies: if a single hub orders and aggregates what every place sends, it becomes the point where power and attacks concentrate. What a network of local AIs should keep distributed is not only capability but the independence of each place's judgment.

## How this relates to existing work

Each part of this argument has precedents. What is new here is putting them in one picture.

- **Bandwidth and BMIs.** Elon Musk has long argued that human output bandwidth is pitifully low and that BMIs are the path to human–AI symbiosis. Pugnet's Phase Lock develops a fuller version, and explicitly concedes that the binding constraint may be comprehension rather than communication; his answer is to expand cognition itself, through neural augmentation and whole-brain emulation. This essay agrees on the diagnosis but not the remedy: even copies of ourselves still have to come back.
- **The central bottleneck.** [Zheng & Meister](https://arxiv.org/abs/2408.10234v2) estimate human behavioral throughput at about 10 bits per second. Herbert Simon made the institutional version of the point in 1971: a wealth of information creates a poverty of attention, and organizations must be designed around that scarcity.
- **BMIs and agents together.** [Meunier et al. (2024)](https://arxiv.org/abs/2402.15011) propose brain–artificial intelligence interfaces, in which the user supplies high-level intent from EEG and an AI agent fills in the details. [Chen et al.](https://arxiv.org/abs/2510.22095) call for a shift from brain–computer interfaces to brain–agent collaboration, with intent clarification, user agency and governance built in. Both match the division of labor here — BMI for intent, agents for the rest — but stop before the return.
- **Attention as the bottleneck for agents.** Practitioners running many coding agents report the same limit from the other side: the constraint is not the agents but the developer's attention, as in Zack Proser's talk [Your attention is the bottleneck, not your agents](https://www.ai.engineer/talks/so9l_MwS2yg-your-attention-is-bottleneck-not-your-agents) (AI Engineer Europe 2026).
- **Governing agents.** OpenAI's [Practices for Governing Agentic AI Systems](https://openai.com/index/practices-for-governing-agentic-ai-systems/) (Shavit et al., 2023) proposes constraining the action space and requiring approval, legibility of agent activity, automatic monitoring, attributability, and interruptibility. These map onto access governance and onto the provenance side of the return; the cost of reading what they produce is what this essay adds.
- **Blockchain scaling.** Layer-2 rollups, data availability, and EIP-4844's pruned blobs are the most concrete existing price for the B–C trade-off; the analogy above borrows from that engineering literature rather than claiming anything new about it.
- **Privacy.** Helen Nissenbaum's contextual integrity frames privacy as appropriate information flow rather than secrecy. Neurorights are now entering law: Chile wrote them into its constitution in 2021, and UNESCO adopted a Recommendation on the Ethics of Neurotechnology in 2025. Pugnet's Phase Lock proposes on-device processing, transmitting intent rather than raw signals, and consent that expires unless renewed.
- **Data from places.** The Nagoya Protocol governs access to genetic resources and the sharing of their benefits, and the 2024 UN biodiversity conference (COP16) set up a fund for benefits from digital sequence information. The CARE Principles for Indigenous Data Governance (collective benefit, authority to control, responsibility, ethics) state the conditions under which community data stays accountable to its source. Federated learning offers a technical route for learning across places without pooling raw data.
- **Provenance and memory.** Data provenance has standards such as W3C PROV. In psychology, source-monitoring research (Johnson, Hashtroudi & Lindsay, 1993) studies how people lose track of where a memory came from — the human form of source amnesia. Transactive memory (Wegner) and organizational memory (Walsh & Ungson, 1991) describe how groups store knowledge across members. Archival appraisal and retention scheduling come from archival science. Conway's law (1968) — systems mirror the communication structure of the organizations that build them — suggests that how we allot integration bandwidth among clones will shape what the merged self becomes.

## Summary

People want two things from AI: to draw out, and to act. BMIs widen the bandwidth of expression; agents widen the bandwidth of action. Widen both, and the bandwidth of reception becomes the problem — the shadow clone problem.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig4.svg" alt="A loop between a person and AI agents: expression bandwidth widened by BMIs on the way out, action bandwidth widened by agents, and reception bandwidth on the way back as the bottleneck where institutions are needed." loading="lazy"><figcaption>Figure 5. The three bandwidths, and the loop that has to be designed</figcaption></figure>

Faster interfaces do not remove it, and neither does faster cognition. Copying ourselves multiplies it: more clones, more experience coming back, the same single point of return. And it holds just as well when the one receiving is not a person but a place. So the return path has to be designed, not assumed. The harness gives one mechanism to each moment of the clone's life: access governance for acting, reporting governance for choosing what comes back and how, and memory governance for what is kept, what is let go, and who may see it.

What matters is designing the estimation and confirmation of intent, execution within the scope of granted authority, verification of results, and reporting back to the human as a single loop. BMIs and AI agents can complement each other within that loop — as long as we take responsibility for what comes home.
