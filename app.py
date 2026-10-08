"""Streamlit interface for the Rosa's Pizza assignment.

The two calculation functions are reused from the uploaded assignment file.
The web interface was generated with Codex using notebook-to-streamlit.
"""

import numpy as np
import streamlit as st
from starter import ZONES, TIME_BLOCKS, COSTS, delivery_times


# Calculation functions copied from the assignment file.
def late_order_loss(costs):
    return costs["refund"] + costs["churn_orders"] * costs["margin"]


def find_best_promise(zone, time_block, promises, costs, seed=1):
    best_promise = None
    best_profit = -np.inf
    results = []
    late_cost = late_order_loss(costs)

    for promise in sorted(promises):
        times = delivery_times(
            zone, time_block, promise, seed=seed
        )

        orders = len(times)
        late_orders = np.sum(times > promise)
        profit = orders * costs["margin"] - late_orders * late_cost

        results.append((promise, orders, late_orders, profit))

        if profit > best_profit:
            best_promise = promise
            best_profit = profit

    return best_promise, best_profit, results


def main():
    st.set_page_config(page_title="Rosa's Pizza", layout="centered")
    st.title("Rosa's Pizza: Delivery Promise")
    st.write("Find the delivery promise with the highest simulated net profit.")
    st.caption("All order counts and profits cover four weeks.")

    with st.form("promise_inputs"):
        zone_column, block_column = st.columns(2)
        with zone_column:
            zone = st.selectbox("Zone", ZONES, index=ZONES.index("Far West"))
        with block_column:
            time_block = st.selectbox(
                "Time block", TIME_BLOCKS, index=TIME_BLOCKS.index("Fri/Sat eve")
            )

        st.write("Delivery promises to compare (minutes)")
        min_column, max_column = st.columns(2)
        with min_column:
            min_promise = st.number_input(
                "Minimum promise", min_value=5, value=15, step=5
            )
        with max_column:
            max_promise = st.number_input(
                "Maximum promise", min_value=5, value=75, step=5
            )
        st.caption("Both endpoints are included. Enter multiples of 5.")

        st.write("Costs")
        margin_column, churn_column, refund_column = st.columns(3)
        with margin_column:
            margin = st.number_input(
                "Margin per order ($)", min_value=0.0,
                value=float(COSTS["margin"]), step=0.1, format="%.2f"
            )
        with churn_column:
            churn_orders = st.number_input(
                "Orders lost per late order", min_value=0.0,
                value=float(COSTS["churn_orders"]), step=0.1, format="%.2f"
            )
        with refund_column:
            refund = st.number_input(
                "Refund per late order ($)", min_value=0.0,
                value=float(COSTS["refund"]), step=0.1, format="%.2f"
            )

        submitted = st.form_submit_button("Find best promise")

    if submitted:
        if min_promise > max_promise:
            st.error("Minimum promise must be less than or equal to maximum promise.")
            return
        if min_promise % 5 != 0 or max_promise % 5 != 0:
            st.error("Enter multiples of 5 for both promise limits.")
            return

        # Keep the starter package's COSTS unchanged.
        user_costs = {
            "margin": margin,
            "churn_orders": churn_orders,
            "refund": refund,
        }
        promises = list(range(min_promise, max_promise + 1, 5))
        best_time, best_profit, results = find_best_promise(
            zone, time_block, promises, user_costs, seed=1
        )

        promise_column, profit_column = st.columns(2)
        with promise_column:
            st.metric("Recommended promise", f"{best_time} minutes")
        with profit_column:
            st.metric("Net profit over four weeks", f"${best_profit:,.2f}")

        for promise, orders, late_orders, profit in results:
            if promise == best_time:
                st.write(
                    f"At this promise: {orders} orders, including {int(late_orders)} late deliveries."
                )
        st.write(f"Loss per late order: ${late_order_loss(user_costs):,.2f}")

        table = []
        for promise, orders, late_orders, profit in results:
            table.append({
                "Promise (minutes)": promise,
                "Orders": orders,
                "Late orders": int(late_orders),
                "Net profit ($)": round(float(profit), 2),
            })
        st.dataframe(table, hide_index=True)

        if best_time == min_promise or best_time == max_promise:
            st.info(
                "The best tested promise is at an endpoint. Try a wider range to check for a better option."
            )
        st.caption(
            "This recommendation applies to the selected zone, time block, costs, and tested promises."
        )


if __name__ == "__main__":
    main()
