from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import time


"""
# Loan analyze

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
""
"""In order to make a profit, the interest rate must cover both profit margins,
operational costs, and cover for unpaid loans. 

This means that we can compute exactly how much margins we have for our model.
"""


with st.echo("below"):
    col1, col2, col3, = st.columns(3)


    central_interest = col1.slider("Central Bank interest rate in %", 0., 10., 4., 0.25) / 100
    loan_size = col2.slider("Size of avg loan in $", 100, 500, 300, 50)
    default_rate = col3.slider("Default rate %", 0., 30., 10., 0.5) / 100

    op_cost = col1.slider("Operational cost in %", 0., 10., 2., 0.5) / 100
    profit_margin = col2.slider("profit margins in %", 0., 5., 1., 0.1) / 100
    num_months = col3.slider("avg number of month until payment", 1, 12, 3, 1) / 12
    losses = - loan_size * default_rate

    risk_margin = default_rate / (1 - default_rate)
    col1.write(f"### Risk Margin: {risk_margin * 100:.3f}%")


    income = loan_size * profit_margin * (1 - default_rate)
    col2.write(f"### Bank profits per loan: {income:.2f}")

    total_interest = (risk_margin + op_cost + profit_margin + central_interest) * 100
    col3.write(f"### Total loan interest: {total_interest:.2f}%")

    risk_reduction = col1.slider("RiceUP risk reduction in %", 0.001, default_rate * 100, 0.001, 0.1) / 100
    new_default_rate = default_rate - risk_reduction
    # default_rate
    # risk_reduction
    new_risk_margin = new_default_rate / (1 - new_default_rate)

    # if risk_reduction > 0:
    riceup_commission = col2.slider("RiceUP commision in %", 0., (risk_margin - new_risk_margin) * 100, 0., 0.1) / 100
    # else:
    #     riceup_commission = 0

    margin_left = risk_margin - new_risk_margin - riceup_commission

    increased_profit_margin = col3.slider("Bank Increased profit margins in %", 0., margin_left*100, 0., 0.1) / 100


    final_interest = (
        new_risk_margin + op_cost + profit_margin + increased_profit_margin + central_interest + riceup_commission) * 100

    col1.write(f"### Final RiceUP profit per loan: {loan_size * riceup_commission:.2f}$")
    col2.write(f"### Final bank profit per loan: {loan_size * (profit_margin + increased_profit_margin) * (1 - new_default_rate):.2f}$")
    col3.write(f"### Final loan interest rate: {final_interest:.2f}%")

    col1.write(f"### Money saved for the farmer: {loan_size * (total_interest - final_interest) / 100:.2f}$")
    col1, col2, col3, = st.columns(3)

    options_num_farmers = [1e1,5e1, 1e2, 5e2, 1e3, 5e3, 1e4, 5e4, 1e6, 5e6, 1e7, 5e7, 1e8]

    num_farmers = col2.select_slider("Number of Farmers", options_num_farmers)
    col1, col2, col3, = st.columns(3)
    col1.write(f"### Final RiceUP profit: {num_farmers * loan_size * riceup_commission:,.2f}$")
    col2.write(f"### Final bank profit: {num_farmers * loan_size * (profit_margin + increased_profit_margin) * (1 - new_default_rate):,.2f}$")
    col3.write(f"### Money saved for all farmers: {num_farmers * loan_size * (total_interest - final_interest) / 100:,.2f}$")


# with st.echo(code_location='above'):
# total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
# num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

# Point = namedtuple('Point', 'x y')
# data = []

# points_per_turn = total_points / num_turns

# for curr_point_num in range(total_points):
#     curr_turn, i = divmod(curr_point_num, points_per_turn)
#     angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#     radius = curr_point_num / total_points
#     x = radius * math.cos(angle)
#     y = radius * math.sin(angle)
#     data.append(Point(x, y))

# st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#                 .mark_circle(color='#0068c9', opacity=0.5)
#                 .encode(x='x:Q', y='y:Q'))
