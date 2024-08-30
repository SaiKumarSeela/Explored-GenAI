import mlflow
import os
import pandas as pd
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os              

load_dotenv()

# Prepare evaluation data
eval_data = pd.DataFrame(
    {
        "inputs": [
            "What is MLflow?",
            "What is Spark?",
        ],
        "ground_truth": [
            "MLflow is an open-source platform for managing the end-to-end machine learning (ML) "
            "lifecycle. It was developed by Databricks, a company that specializes in big data and "
            "machine learning solutions. MLflow is designed to address the challenges that data "
            "scientists and machine learning engineers face when developing, training, and deploying "
            "machine learning models.",
            "Apache Spark is an open-source, distributed computing system designed for big data "
            "processing and analytics. It was developed in response to limitations of the Hadoop "
            "MapReduce computing model, offering improvements in speed and ease of use. Spark "
            "provides libraries for various tasks such as data ingestion, processing, and analysis "
            "through its components like Spark SQL for structured data, Spark Streaming for "
            "real-time data processing, and MLlib for machine learning tasks",
        ],
    }
)

mlflow.set_experiment("LLM Evaluation")

# Start an MLflow run
with mlflow.start_run() as run:
    system_prompt = "Answer the following question in two sentences"
    
    # Initialize the Hugging Face Inference Client
    client = InferenceClient(model="mistralai/Mistral-Nemo-Instruct-2407", token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

    # Define a function to get responses from the Llama model
    def get_response(question):
        response = client.text_generation(
            prompt=f"System: {system_prompt}\nHuman: {question}\nAssistant:",
            max_new_tokens=500,
            temperature=0.7,
            do_sample=True,
        )
        return response

    # Evaluate the model using predefined metrics
    results = []
    for index, row in eval_data.iterrows():
        answer = get_response(row['inputs'])
        results.append({
            "input": row['inputs'],
            "predicted": answer,
            "ground_truth": row['ground_truth']
        })

    # Convert results to DataFrame for evaluation
    results_df = pd.DataFrame(results)

    # Save results to a CSV file and log it as an artifact
    csv_path = 'eval.csv'
    results_df.to_csv(csv_path, index=False)
    mlflow.log_artifact(csv_path)

    print(f"See evaluation results below: \n{results_df}")
