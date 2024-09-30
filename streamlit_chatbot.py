import streamlit as st
import google.generativeai as genai

if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = None 

st.title("LLM to SQL command")
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

if "greeted" not in st.session_state:
    st.session_state.greeted = False 

if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
    except Exception as e:
        st.error(f"Error configuring Gemini API Key: {e}")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, message in st.session_state.chat_history:
        st.chat_message(role).markdown(message)

    if not st.session_state.greeted:
        greeting_prompt = "Greet the user as a friendly and knowledgeable dataengineer. \
                        Introduce yourself (you are AI assistant) and let the user know you're here to assist with \
                        any questions they may have about the transformation user questions into SQL queries to retrieve data from a BigQuery database."

        try:
            response = model.generate_content(greeting_prompt)
            bot_response = response.text
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
            st.session_state.greeted = True
        except Exception as e:
            st.error(f"Error generating AI greeting: {e}")

    if user_input := st.chat_input("Type your message here..."):
        st.session_state.chat_history.append(("user", user_input))
        st.chat_message("user").markdown(user_input)

        try:
            prompt = """You are an AI assistant that transforms user questions into SQL queries to retrieve data from a BigQuery database. 
                    Below is the detailed schema of the database, including table names, column names, data types, and descriptions. 
                    Use this information to generate accurate SQL queries based on user input. 
                    ### Data Dictionar 
                    # #### Table: Customers 
                    | Column Name      | Data Type   | Description                                 | 
                    |------------------|-------------|---------------------------------------------| 
                    | customer_id      | INT64       | The unique ID of the customer (Primary Key) | 
                    | first_name       | STRING      | The first name of the customer              | 
                    | last_name        | STRING      | The last name of the customer               | 
                    | email            | STRING      | The email address of the customer           | 
                    | phone_number     | STRING      | The phone number of the customer            | 
                    | registration_date| DATE        | The date the customer registered            | 
                    #### Table: Orders 
                    | Column Name      | Data Type   | Description                                 | 
                    |------------------|-------------|---------------------------------------------| 
                    | order_id         | INT64       | The unique ID of the order (Primary Key)    | 
                    | customer_id      | INT64       | The ID of the customer who made the order (Foreign Key to Customers) | 
                    | order_date       | DATE        | The date when the order was placed          | 
                    | total_amount     | FLOAT64     | The total amount for the order              | 
                    | order_status     | STRING      | The current status of the order (e.g., pending, completed, canceled) | 
                    #### Table: Products 
                    | Column Name      | Data Type   | Description                                 | 
                    |------------------|-------------|---------------------------------------------| 
                    | product_id       | INT64       | The unique ID of the product (Primary Key)  | 
                    | product_name     | STRING      | The name of the product                     | 
                    | category         | STRING      | The category of the product                 | 
                    | price            | FLOAT64     | The price of the product                    | 
                    | stock_quantity   | INT64       | The quantity of the product in stock        | 
                    #### Table: OrderDetails 
                    | Column Name      | Data Type   | Description                                 | 
                    |------------------|-------------|---------------------------------------------| 
                    | order_detail_id  | INT64       | The unique ID of the order detail (Primary Key) | 
                    | order_id         | INT64       | The ID of the order (Foreign Key to Orders) | 
                    | product_id       | INT64       | The ID of the product (Foreign Key to Products) | 
                    | quantity         | INT64       | The quantity of the product ordered         | 
                    | price_per_unit   | FLOAT64     | The price per unit of the product           | 
                    #### Table: Payments 
                    | Column Name      | Data Type   | Description                                 | 
                    |------------------|-------------|---------------------------------------------| 
                    | payment_id       | INT64       | The unique ID of the payment (Primary Key)  | 
                    | order_id         | INT64       | The ID of the order (Foreign Key to Orders) | 
                    | payment_date     | DATE        | The date the payment was made               | 
                    | payment_amount   | FLOAT64     | The amount of the payment                   | 
                    | payment_method   | STRING      | The method used for payment (e.g., credit_card, paypal) | 
                    ### Relationships between tables: 
                    - `Orders.customer_id` references `Customers.customer_id`. 
                    - `OrderDetails.order_id` references `Orders.order_id`. 
                    - `OrderDetails.product_id` references `Products.product_id`. 
                    - `Payments.order_id` references `Orders.order_id`. \n
                    """

            for role, message in st.session_state.chat_history:
                prompt += f"{role}: {message}\n"

            prompt += f"User: {user_input}\n"

            prompt += """"Based on the user's input, generate an appropriate SQL query to retrieve the requested information from the database. 
                    Be precise and ensure that the query follows SQL syntax correctly."""

            response = model.generate_content(prompt)
            bot_response = response.text

            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)

        except Exception as e:
            st.error(f"Error generating AI response: {e}")