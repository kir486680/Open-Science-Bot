
#let datasheet(
    company: (
        name:           "Diode Inc.",
        logo:           "./diode-logo.svg",
        website_url:    "https://github.com/diodeinc",
    ),
    metadata: (
        title: [YourDSTitle],
        product: [YourProductName],
        product_url: "https://github.com/diodeinc",
        revision: [CurrentRevision],
        publish_date: [PublishedOn]
    ), features: [], applications: [], desc: [], revisions: [], doc: [], notes: []) = {

    let fonts = (
        serif:          ("Tinos", "Roboto", "Inter"),
        sans:           ("Inter", "Roboto"),
        mono:           ("Fira Mono", "IBMPlexMono"),
        text:           ("Inter", "Roboto", "Raleway"),
        text_strong:    ("Inter", "Roboto"),
        headings:       ("Roboto", "Inter", "Tinos"),
        code:           ("Fira Code", "IBMPlexMono"),
    )

    set text(font: fonts.text, size: 11pt)
    show link: it => text(fill: rgb("#0000FF"))[#it]
    set page(paper: "a4")

    // Figure styles
    show figure.caption: set text(
        weight: "semibold",
        font: fonts.headings
    )

    // table styles
    show figure.where(
        kind: table
    ): set figure.caption(position: top)

    set table(
        stroke: 0.5pt,
        fill: (_, y) => if y == 0 { gray.lighten(75%) },
        align: (_, y) => if y == 0 { align(center) },
    )
    show table.header: strong
    show table.cell.where(y: 0): set text(weight: "semibold")
    let lastest_rev = revisions.last()

    let outline_page() = {
        [
            #block(height: 40%, [
                #columns(2, gutter: 30pt)[
                    = Contents
                    <Directory>
                    #outline(title: none, depth: 3)
                ]
            ])

            #line(length: 100%, stroke: 1pt)
        ]
    }

    let revisions_page() = {
        [
            = Revisions

            <Revisions>

            #v(1em)

            #block({
                for r in revisions {
                    text(font: fonts.sans, weight: "semibold", [#r.rev - #r.date])
                    v(-0.65em)
                    line(length: 100%, stroke: 0.3pt)
                    v(-0.65em)
                    block(r.body)
                    v(-0.65em)
                    line(length: 100%, stroke: 0.65pt)
                    v(0.65em)
                }
            })
        ]
    }


    let notes_page() = {
        [
            = Notes

            <Notes>

            #v(1em)

            #block({
                for n in notes {
                    text(font: fonts.sans, weight: "semibold", [#n.note - #n.date])
                    v(-0.65em)
                    line(length: 100%, stroke: 0.3pt)
                    v(-0.65em)
                    block(n.body)
                    v(-0.65em)
                    line(length: 100%, stroke: 0.65pt)
                    v(0.65em)
                }
            })
        ]
    }

    let page_footer() = {
        line(length: 100%, stroke: 1pt)
        v(-0.65em)
        set text(10pt, baseline: 0pt)
        locate(loc => if calc.odd(loc.page()) {
                grid(
                    columns: (5fr, 1fr),
                    rows: (auto),
                    gutter: 0pt,
                    [Copyright © #link(company.website_url)[#company.name]],
                    [
                        #set align(right)
                        #counter(page).display("1 / 1", both: true)
                    ],
                )
            } else {
                grid(
                    columns: (1fr, 5fr),
                    rows: (auto),
                    gutter: 0pt,
                    [
                        #set align(left)
                        #counter(page).display("1 / 1", both: true)
                    ],
                    [
                        #set align(right)
                        Copyright © #link(company.website_url)[#company.name]],
                )
            }
        )
    }

    let current_chapter() = locate(loc => {
        let elems = query(
            heading.where(level:2).before(loc),
            loc,
        )
        if elems != () {
            let elem = elems.last()
            h(1fr) + emph(counter(heading).at(loc).map(str).join(".") + h(.75em) + elem.body) + h(1fr)
        }
    })

    let afterwords_page() = {

        set page(numbering: none)

        set heading(numbering: none)

        [
            = Indexing

            #box(height: auto, [
                #columns(2, gutter: 30pt)[
                    #outline(
                        title: [Figures],
                        target: figure.where(kind: image),
                    )
                    #colbreak()
                    #outline(
                        title: [Tables],
                        target: figure.where(kind: table),
                    )
                ]
                #line(length: 100%, stroke: 1pt)
            ])

            = Legal Disclaimer Notice

            #lorem(30)

            #lorem(50)

            #lorem(30)
        ]

    }

    set par(leading: 0.75em)

    set page(
        numbering: "(1 / 1)",
        footer-descent: 2em,
        header: [
            #set text(10pt)
            #locate(loc => if calc.odd(loc.page()) {
                    grid(
                        columns: (1fr, 1fr),
                        rows: (100%),
                        gutter: 3pt,
                        [
                            #set align(left)
                            #link(company.website_url)[#image(company.logo, height: 18pt)]
                        ],
                        [
                            #set align(right)
                            #link(metadata.product_url)[#metadata.product]
                            #linebreak()
                            #lastest_rev.rev - #lastest_rev.date
                        ],
                    )
                } else {
                    grid(
                        columns: (1fr, 1fr),
                        rows: (100%),
                        gutter: 3pt,
                        [
                            #set align(left)
                            #link(metadata.product_url)[#metadata.product]
                            #linebreak()
                            #lastest_rev.rev - #lastest_rev.date
                        ],
                        [
                            #set align(right)
                            #link(company.website_url)[#image(company.logo, height: 18pt)]
                        ],
                    )
                }
            )
            #v(-0.65em)
            #line(length: 100%, stroke: 1pt)
        ],
        footer: page_footer(),
        background: if metadata.confidential {
            rotate(45deg,
               text(70pt, fill: rgb("FFCBC4"))[
             *CONFIDENTIAL*
            ])
        }
    )

    set heading(numbering: "1.")

    show heading: it => block([
        #v(0.3em)
        #text(weight: "bold", font: fonts.headings, [#counter(heading).display() #it.body])
        #v(0.8em)
    ])

    show heading.where(level: 1): it => {
        block([
            #text( weight: "bold", font: fonts.headings, [#counter(heading).display() #it.body])
            #v(0.3em)
        ])
    }

    v(-0.65em)
    align(center, block({
        set text(16pt, font: fonts.headings, weight: "medium")
        metadata.title
        v(-0.5em)
        line(length: 100%, stroke: 1pt)
        v(0.3em)
    }))

    box(height: auto,
        columns(2, gutter: 30pt)[

= Features
<TitlePageFeatures>

#features

= Applications
<TitlePageApplications>

#applications

#colbreak()

= Description
<Description>

#desc

    ])
        pagebreak()
        outline_page()

    if notes.len() != 0 {
        pagebreak()
        notes_page()
    }

    if revisions.len() != 0 {
        pagebreak()        
        revisions_page()
    }

    pagebreak()

    // document-body
    doc

    afterwords_page()
}