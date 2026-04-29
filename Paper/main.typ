#import "@preview/charged-ieee:0.1.4": ieee
#import "@preview/wordometer:0.1.5": word-count, total-words

#show: word-count.with(exclude: (
  bibliography, 
  figure.caption,
))

#show: ieee.with(
  title: [Impact of Instruction Set Architecture on Performance and Energy Efficiency in Modern Computing],
  authors: (
    (
      name: "Student X",
      department: [High School Y],
      organization: [Word Count: #total-words],
    ),
  ),
  bibliography: bibliography("refs.bib"),
  figure-supplement: [Fig.],
)

#include("content/introduction.typ")
#include("content/lit_review.typ")
#include("content/methodology.typ")
#include("content/results.typ")
#include("content/limitations.typ")
