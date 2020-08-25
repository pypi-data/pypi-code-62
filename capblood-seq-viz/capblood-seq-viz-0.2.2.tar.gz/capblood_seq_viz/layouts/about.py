import dash_html_components as html
import dash_bootstrap_components as dbc


def about_layout():
    return dbc.Container(
        html.Div(
            [
                html.P(
                    children=[
                        "This is a companion web app to the project, \"Scaling human immunity studies via single-cell profiling of capillary blood\", from the ",
                        html.A("Thomson Lab", href="http://thomsonlab.caltech.edu/"),
                        " at Caltech"
                    ]
                ),
                html.P(
                    "The immune system, driven by complex interactions betweens cells and genes, is unique to each individual and varies over time due to environmental factors  and genetic predispositions."
                ),
                html.P(
                    "Understanding these temporal and inter-individual differences in context of gene expression has the potential to evaluate one's disease risk and guide development of personalized medicine. We developed a pipeline that uses multiplexed single-cell sequencing and out-of-clinic capillary blood extraction to get easily accessible insights into transcriptomic changes underlying these differences. To validate our technology, we conducted a three day study consisting of 4 healthy adults in which we collected capillary blood in the morning (AM) and evening (PM). We found numerous genes that exhibit diurnal expression across subjects and in unique immune cell subpopulations, as well as plethora of genes that are subject and cell type specific."
                ),
                html.P(
                    "Given the highly-dimensional nature of the data, we created this web portal for exploration of our findings."
                ),
                html.P(
                    children=[
                        "To see the raw data used to generate these analysis: ",
                        html.A("https://data.caltech.edu/records/1407", href="https://data.caltech.edu/records/1407")
                    ]
                ),
                html.P(
                    children=[
                        "To see the code used generate these analysis: ",
                        html.A("https://github.com/thomsonlab/capblood-seq",
                               href="https://github.com/thomsonlab/capblood-seq")
                    ]
                ),
                html.P(
                    children=[
                        "And the visualization you see here: ",
                        html.A("https://github.com/thomsonlab/capblood-seq-viz",
                               href="https://github.com/thomsonlab/capblood-seq-viz")
                    ]
                )
            ],
            className="col-sm-8",
            id="about_container"
        )
    )
