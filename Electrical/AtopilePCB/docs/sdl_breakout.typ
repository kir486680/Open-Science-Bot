#import "@preview/gentle-clues:0.6.0": warning, error
#import "@preview/cetz:0.1.2": canvas, plot

#import "assets/diode-ds.typ": datasheet
#import "revisions.typ": revisions
#import "notes.typ": notes

#let company = (
    name:           "", // TODO: Replace with actual company name
    logo:           "./diode-logo.svg",
    website_url:    "", // TODO: Replace with actual website
)

#let metadata = (
    title: [SdlBreakout],
    product: "", // TODO: Replace with actual product number
    product_url: "", // TODO: Replace with actual product URL
    confidential: false,
)

#let features = [
    // TODO: Replace with actual features
]


#let applications = [
    // TODO: Replace with actual applications
]

#let desc = [
    // TODO: Replace with actual description
]

#show: doc => datasheet(
    company: company,
    metadata: metadata,
    features: features,
    applications: applications,
    desc: desc,
    revisions: revisions,
    notes: notes,
    doc: doc
)

= Specifications

== Pin Configuration and Functions
<PinConfigAndFunctions>

// TODO: Replace with actual pin configuration and functions

== Specifications
<Specifications>

// TODO: Replace with actual specifications

== Absolute Maximum Ratings
<AbsoluteMaximumRatings>

// TODO: Replace with actual absolute maximum ratings

#pagebreak()

= Detailed Description
<DetailedDescription>

== Overview

// TODO: Replace with actual overview

== Functional Block Diagram

// TODO: Replace with actual functional block diagram

#pagebreak()

= Application and Implementation

=== Application Information

// TODO: Replace with actual application information

=== Typical Applications

// TODO: Replace with actual typical applications

=== Design Requirements

// TODO: Replace with actual design requirements

= Power Supply Recommendations

// TODO: Replace with actual power supply recommendations

=== PCB Layout

// TODO: Replace with actual PCB layout

#pagebreak()

= Device and Documentation Support

=== Device Support

=== Related Links

// TODO: Replace with actual related links. If available, add links to datasheets, application notes, etc.

#pagebreak()
  
= Mechanical, Packaging, and Orderable Information

// TODO: Replace with actual mechanical, packaging, and orderable information