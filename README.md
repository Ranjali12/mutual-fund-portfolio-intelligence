# Mutual Fund Portfolio Intelligence

A small AI-powered prototype that helps an investor understand their mutual fund portfolio.

The idea behind this project is simple: instead of asking an LLM to directly analyse raw financial data, I first perform the important calculations and validation deterministically, and then use Gemini to turn those verified results into useful, prioritised insights.

---

## What does this project do?

The system takes a structured investor profile and mutual fund portfolio as input and answers:

> **What are the most important things this investor should know about their portfolio, and why?**

It currently looks at things such as:

- Portfolio value
- Investment cost
- Profit/loss
- Returns
- Portfolio allocation
- Concentration
- Data-quality issues
- Investor risk profile
- Investment horizon
- Investment goal

It then uses Gemini to generate a small number of personalised insights based only on the verified analysis.

---

## Why I built it this way

I intentionally separated **financial calculations** from **LLM reasoning**.

I don't want an LLM deciding what `50 × ₹2,281.78` is or inventing a NAV.

Instead:

**Python handles the numbers and validation.**

**Gemini handles interpretation and explanation.**

This makes the system easier to test and reduces the chance of unsupported financial claims.

---

## How it works

```text
Investor Portfolio JSON
          |
          v
     Input Loader
          |
          v
   AMFI NAV Data
          |
          v
     Fund Matcher
          |
          v
 Deterministic Analytics
   |       |       |
   |       |       +--> Concentration
   |       +----------> Allocation
   +------------------> P/L & Returns
          |
          v
    Data Quality Checks
          |
          v
   Verified Portfolio Data
          |
          v
   Gemini Insight Generator
          |
          v
       CLI Output
