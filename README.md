# 2D Ising Model Solution using Metropolis-Hastings MCMC

## Introduction

This repository contains a numerical solution to the 2D Ising model using the Metropolis-Hastings Monte Carlo method. The Ising model is a mathematical model in statistical mechanics that describes the behavior of spins on a lattice, where each spin can be in one of two states. This model is used to study phase transitions and critical phenomena.

### Monte Carlo Simulations

Monte Carlo simulations are a class of computational algorithms that rely on repeated random sampling to obtain numerical results. These simulations are particularly useful for systems with a large number of coupled degrees of freedom, such as spin systems in statistical mechanics. The key idea is to use randomness to explore the state space of the system and to estimate properties like average energy, magnetization, and specific heat.

### Markov Chain and Detailed Balance

A Markov Chain is a stochastic process that undergoes transitions from one state to another on a state space. It is characterized by the property that the future state depends only on the current state and not on the sequence of events that preceded it.

- **Steady State:** A Markov Chain reaches a steady state when the probability distribution of states does not change over time. In other words, the system reaches equilibrium.
  
- **Detailed Balance:** Detailed balance is a condition that ensures the system is in equilibrium. It states that for every pair of states \(i\) and \(j\), the rate of transition from \(i\) to \(j\) is equal to the rate of transition from \(j\) to \(i\). Mathematically, this is expressed as:
  \[
  \pi_i p_{ij} = \pi_j p_{ji}
  \]
  where \(\pi_i\) and \(\pi_j\) are the steady-state probabilities of states \(i\) and \(j\), respectively, and \(p_{ij}\) and \(p_{ji}\) are the transition probabilities between these states.

### The Ising Model

#### 1D Ising Model

The 1D Ising model consists of spins arranged in a linear chain, where each spin can interact with its nearest neighbors. It is known that the 1D Ising model does not exhibit a phase transition at any finite temperature. This is because thermal fluctuations dominate over spin-spin interactions, preventing long-range order.

#### 2D Ising Model with Periodic Boundary Conditions

The 2D Ising model extends the 1D model to a two-dimensional lattice, where each spin interacts with its four nearest neighbors. Unlike the 1D model, the 2D Ising model does exhibit a phase transition at a critical temperature. Below this temperature, the system exhibits spontaneous magnetization, while above it, the system is in a disordered phase.

In this repository, we consider a 2D lattice with periodic boundary conditions, meaning that the lattice edges are connected to form a continuous surface without boundaries. This approach reduces edge effects and better simulates an infinite system.

## Metropolis-Hastings Algorithm

The Metropolis-Hastings algorithm is a widely used Markov Chain Monte Carlo method for sampling from a probability distribution. The key steps in the algorithm are:

1. **Initialization:** Start with an initial configuration of spins.
2. **Proposal:** Randomly select a spin and propose to flip it.
3. **Acceptance:** Calculate the change in energy due to the proposed flip. Accept the flip with a probability that depends on the change in energy and the temperature of the system (Boltzmann factor):
   \[
   p_{ij} = P(r_1 | \sigma_i) = g(r_1 | \sigma_i) A(\sigma_j | \sigma_i)
   \]
   where \( g(r_1 | \sigma_i) \) is the probability of the proposal, and \( A(\sigma_j | \sigma_i) \) is the probability of accepting the proposal.
4. **Iteration:** Repeat the proposal and acceptance steps for a large number of iterations to allow the system to reach equilibrium.

By iterating this process, the algorithm generates a sequence of spin configurations that sample the equilibrium distribution of the system.

### Detailed Balance in Metropolis-Hastings

Say that we propose a state \(\sigma_j\) given that our system is currently at state \(\sigma_i\). We know the transition probability is \(p_{ij}\). The probability of this transition occurring is given by:
\[
p_{ij} = P(r_1 | \sigma_i) = g(r_1 | \sigma_i) A(\sigma_j | \sigma_i)
\]
where \(g(r_1 | \sigma_i)\) is the probability of the proposition, and \(A(\sigma_j | \sigma_i)\) is the probability of accepting the said proposal.

Replacing this expression in the detailed balance equation, we get:
\[
\pi_i g(r_1 | \sigma_i) A(\sigma_j | \sigma_i) = \pi_j g(r_1 | \sigma_j) A(\sigma_i | \sigma_j)
\]
Additionally, we know that the steady-state probability for each state is given by the Boltzmann distribution:
\[
\pi_i = \frac{e^{-\beta \mathcal{H}(\sigma_i)}}{Z}
\]
Substituting this into the detailed balance condition, we obtain:
\[
\frac{e^{-\beta \mathcal{H}(\sigma_i)}}{Z} g(r_1 | \sigma_i) A(\sigma_j | \sigma_i) = \frac{e^{-\beta \mathcal{H}(\sigma_j)}}{Z} g(r_1 | \sigma_j) A(\sigma_i | \sigma_j)
\]
Thankfully, we do not need to compute the partition function \(Z\). Moreover, if we set the probability of proposing a given state to be uniform \(1/N\), this simplifies our acceptance ratio, leading us to:
\[
A(\sigma_j | \sigma_i) = \min\left(1, \frac{e^{-\beta \mathcal{H}(\sigma_j)}}{e^{-\beta \mathcal{H}(\sigma_i)}}\right)
\]

#### Simplifying the Acceptance Criterion

We can further simplify by setting one of the acceptance probabilities to 1. The criteria become:
\[
A_{ij} = \begin{cases}
e^{-\beta (\mathcal{H}(\sigma_j) - \mathcal{H}(\sigma_i))} & \text{if } \mathcal{H}(\sigma_j) > \mathcal{H}(\sigma_i) \\
1 & \text{if } \mathcal{H}(\sigma_j) \le \mathcal{H}(\sigma_i)
\end{cases}
\]

This means that the transition from \(\sigma_i\) to \(\sigma_j\) will occur if the energy decreases, or if it passes a probabilistic test valued at \(e^{-\beta (\mathcal{H}(\sigma_j) - \mathcal{H}(\sigma_i))}\).