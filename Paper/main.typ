#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [Impact of Instruction Set Architecture on Performance and Energy Efficiency in Modern Computing],
  authors: (
  ),
  bibliography: bibliography("refs.bib"),
  figure-supplement: [Fig.],
)

#include("content/introduction.typ")
#include("content/lit_review.typ")
#include("content/methodology.typ")
#include("content/results.typ")
#include("content/limitations.typ")
