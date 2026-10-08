---
name: notebook-to-streamlit
description: Use this skill to turn the Rosa's Pizza notebook into a Streamlit app.
---

# Steps

1. Read the local assignment notebook. Reuse late_order_loss and find_best_promise.

2. Use the starter package. Do not change starter.py or its imported constants.

3. Create app.py with dropdowns for zone and time block.

4. Let the user choose a promise range in 5-minute steps. Include both endpoints. Start with 15 to 75 minutes.

5. Let the user adjust margin, churn_orders, and refund. Use COSTS as the defaults and create a separate dictionary for the user's values.

6. Add a button to find the promise with the highest net profit. Show the recommended time and net profit over four weeks.

7. Keep the notebook's simulation logic: simulate each promise separately, use seed=1, and count deliveries as late when time > promise.

8. Create requirements.txt with streamlit, numpy, and git+https://github.com/zhouy185/rosa-starter.git.

9. Run the app and check that the same inputs give the same results as the notebook.