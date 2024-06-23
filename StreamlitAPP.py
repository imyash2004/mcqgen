import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st

from langchain.callbacks import get_openai_callback


with open("/Users/vaibhavagarwal/Desktop/yash/mcqgen/Response.json") as file:
    RESPONSE_JSON=json.load(file)


st.title("MCQ Generator Applocation With Lanchain    ")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("uplaod pdf or txt file")

    mcq_count=st.number_input("No of mcqs ",min_value=3,max_value=50)

    subject=st.text_input("Insert Subject",max_chars=20)
    tone=st.text_input("Complexity of questions ",max_chars=20,placeholder="Simple")
    button=st.form_submit_button("create mcq")


    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading"):
            try:
                text=read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")


                if isinstance(response,dict):

                    quiz=response.get("quiz",None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)

                            st.text_area(label="Review",value=response["review"])

                        else:
                                st.error("Failed to generate quiz")

                else:
                    st.write(response)
                    


  