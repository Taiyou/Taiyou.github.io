---
title: Governance for BMIs and AI Agents · Hiro Taiyo Hamada
description: Brain–machine interfaces widen the bandwidth of expression and AI agents widen the bandwidth of action. Widen both, and a third bottleneck appears — the bandwidth of reception.
label: Blog · 13 September 2026
heading: Governance for BMIs and AI Agents
lead: Brain–machine interfaces widen what we can express. AI agents widen what we can do. Widen both, and a third bottleneck appears — how much one person can take back in.
date: 2026-09-13
original: https://note.com/hirotaiyohamada/n/n003b60d63692
---
<p class="post-origin">This is an English version of an essay first published in Japanese on <a href="https://note.com/hirotaiyohamada/n/n003b60d63692" target="_blank" rel="noopener">note</a> on 13 September 2026.</p>

I have been arguing that **brain–machine interfaces (BMIs)** on their own solve only half the problem, and that we need to invest much more in AI alongside them. Here is a short summary of why.

People want two things from AI.

The first is to **draw out the information inside themselves more richly**.

The second is to **run more work in parallel than they could ever handle alone**.

In the world that is coming, the decoding technology that serves the first need is the **brain–machine interface (BMI)**, and what serves the second is the **AI agent**.

The two are almost never drawn in the same picture. BMIs have been discussed in the context of neural engineering and clinical medicine; agents in the context of software development and multi-agent research. They have been talked about separately.

## The bandwidth of expression and the bandwidth of action

BMIs and agents look like entirely different technologies.

Seen from the human side, though, they are attacking the same problem from opposite directions: the **bandwidth of expression** and the **bandwidth of action**.

Humans have **bandwidth limits**.

When we type on a keyboard or give instructions by voice, we get only a tiny fraction of what is in our heads out into the world — our judgments, where our attention is pointed, intentions that have not yet become words.

This is a limit on the input side: the **bandwidth of expression**.

At the same time, however clear our intentions are, each of us has only one body and one stream of time. We cannot push ten jobs forward at once.

This is a limit on the output side: the **bandwidth of action**.

**BMIs widen the bandwidth of expression; agents widen the bandwidth of action.**

So the two things people want from AI — "draw more out of me" and "do more for me" — correspond to the two ends of a single person's expressive and behavioral constraints.

Framed this way, a question follows naturally:

**How do we hand the rich intent we have extracted to many agents, and how do we bring their results back to one person?**

## BMIs extract intent

Start with the first demand: extraction (Figure 1).

Keyboards and voice are discrete, explicit, and slow.

We first translate what we want to convey into words, and only then type it in. A great deal is lost in that translation.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig1.svg" alt="Two channels lead out of a person's inner state. Keyboard and voice form a narrow, slow channel that yields only a few words; a BMI forms a wide channel that yields rich intent." loading="lazy"><figcaption>Figure 1. BMIs and the bandwidth of expression</figcaption></figure>

What a BMI tries to capture is the continuous, implicit state that exists before that translation: where attention is pointed, what feels off, whether we are hesitating or sure.

The point I want to stress is that the real strength of a BMI lies in **extracting rich intent with as little loss of information as possible**.

One can imagine using a BMI to steer agents directly.

But the job of the BMI is to make the human side's intent denser. Parallelizing and organizing what comes after should be the job of a separate layer.

## Agents take human intent and execute it in parallel

Now the second demand: parallel execution (Figure 2).

As of September 2026, it is fair to say that in most cases agents already exceed the abilities of the average person.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig2.svg" alt="One person's rich intent passes through a harness made of access, memory and reporting governance, then branches out to N agents working in parallel on code, research and documents." loading="lazy"><figcaption>Figure 2. AI agents and the bandwidth of action</figcaption></figure>

They write code, do research, and produce documents. It is already technically possible for dozens of agents to take one person's intent in the form of prompts and carry out separate pieces of work at the same time.

Each agent is given its share of the intent, and the work runs in parallel. The parallel results are then gathered and integrated into a form a human can understand.

This is what is called multi-agent coordination.

Multi-agent coordination is not easy, however. It needs mechanisms for governing how agents behave toward one another.

Human organizations, for example, have mechanisms for keeping information in order: work rules, approval authority, records that are kept, reporting lines. Only with such institutions in place can many people move toward a single goal.

Agents need the same thing. This is what is called a harness.

I think a harness needs three mechanisms:

- **Access governance** — who may access what, and who may decide what.
- **Memory governance** — what is kept, what is discarded, and who inherits that memory.
- **Reporting governance** — what is summarized and abstracted, and in what form results are reported back to the human.

One person's intent passes through the harness, branches out to N agents, and the results come back. That is parallel execution.

## Where the two demands collide

So far I have treated BMIs and agents separately.

But try to satisfy both at once, and there is one place where problems are bound to arise: the integration of information.

Each agent that branches off builds up its own context. Eventually it finishes its work, and that experience flows back to the human.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig3.svg" alt="Results from many agents, each carrying its own context, converge into a funnel that summarizes and abstracts them before a narrow outlet reaches one person." loading="lazy"><figcaption>Figure 3. The bandwidth of reception</figcaption></figure>

At this point the two demands collide.

BMIs have made intent richer, and rich intent produces rich results. Agents have made processing parallel, and parallel processing produces many results.

All of it **floods into the receiving bandwidth of a single person**.

The more we widen the input and output sides, the narrower a person's bandwidth for receiving information becomes in relative terms. This is not a technical shortcoming; it is a third bandwidth problem that follows inevitably from the structure itself.

So whatever comes back has to be summarized and abstracted so that it stays within the limits of human cognition.

What do we throw away, and what do we keep? Do we preserve provenance — who did what, and why it turned out that way — or receive only the results?

This is where AI is needed to integrate and organize information.

Even once we have decided who may see what and what gets kept, the amount one person can take in does not, for now, increase.

There may be a future in which **the amount one person can take in** itself changes — one in which BMIs dramatically improve the brain's capacity for understanding and judgment. Even so, this is likely to remain the bottleneck.

## Summary

People want two things from AI: to draw out, and to act.

<figure class="post-fig"><img src="{{root}}assets/img/blog/bmi-agent-fig4.svg" alt="A loop between a person and AI agents: expression bandwidth widened by BMIs on the way out, action bandwidth widened by agents, and reception bandwidth on the way back as the bottleneck where institutions are needed." loading="lazy"><figcaption>Figure 4. The three bandwidths</figcaption></figure>

These correspond to the two ends of human bandwidth constraints. BMIs widen the **bandwidth of expression**; agents widen the **bandwidth of action**.

And when both are widened, a third bandwidth — the **bandwidth of reception** — inevitably becomes the problem. This is where institutions are needed.

Improving the communication performance of BMIs alone will not necessarily increase the outcomes people actually want.

What matters is designing the estimation and confirmation of intent, execution within the scope of granted authority, verification of results, and reporting back to the human as a single loop.

BMIs and AI agents may complement each other within that loop.
