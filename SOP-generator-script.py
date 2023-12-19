# Importing the necessary libraries

import json
import re
import time
from pandas import json_normalize
from tqdm import tqdm
from pprint import pprint

tqdm.pandas()

from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI


def initialize_api():
    client = OpenAI()

    return client


def NamingCovention():
    name = input("What would you like to name your html file? ")

    return name


def GetUserInput():
    objective = input("What is the objective or purpose of the guideline? ")

    author = input("Who is the author? ")

    audience = input("Who is the intended audience? ")

    format = input("What would be your preferred format of the guideline? ")

    instructions = input(
        "Please provide necessary and additional details that are needed to complete each step. "
    )

    return [objective, author, audience, format, instructions]


def GetMessageMemory(NewQuestion, PreviousResponse, systemContext, client, model_id):
    if PreviousResponse is not None:
        response = client.chat.completions.create(
            model=model_id,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": systemContext},
                {"role": "user", "content": NewQuestion},
                {"role": "assistant", "content": PreviousResponse},
            ],
            temperature=0,
            seed=42,
        )
    else:
        response = client.chat.completions.create(
            model=model_id,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": systemContext},
                {"role": "user", "content": NewQuestion},
            ],
            temperature=0,
            seed=42,
        )

    return response.choices[0].message.content


def run_chat_conversations(client, model_id, context, messages):
    last_response = None
    for user_input in tqdm(messages):
        chat_response = GetMessageMemory(
            user_input, last_response, context, client, model_id
        )
        last_response = chat_response

    return json.loads(last_response)


def GetImages(image_description: str, client):
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_description,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    time.sleep(5)

    return response.data[0].url


def generate_images_and_update_df(df, client):
    df["image_prompt"] = df[df.columns.to_list()[1:]].apply(
        lambda x: "Generate image where "
        + x[0]
        + ". "
        + x[1]
        + ". Name the image as "
        + x[2],
        axis=1,
    )

    df["Example"] = df["image_prompt"].progress_apply(GetImages, client=client)

    return df


def path_to_image_html(path):
    return '<img src="' + path + '" width="200" >'


def main():
    # Initiallizing the openai api object
    client = initialize_api()

    # Defining the variables to be used as inputs in model
    model_id = "gpt-4-1106-preview"
    model_context = "You are an expert Standard Operating Procedure (SOP) generator in a JSON table format.\n \
        Make sure that the instructions given are clear and comprehensive, good enough to generate images as well."
    user_inputs = GetUserInput()

    # Using the given inputs from users, we run them as a loop into the chat function - multi-conversation
    model_responses = run_chat_conversations(
        client, model_id, model_context, user_inputs
    )

    pprint(model_responses)

    # Converting the JSON response for the instructions into a flattened pandas dataframe
    try:
        df = json_normalize(
            model_responses, record_path=["SOP_Table", "Procedure_Steps"]
        )

    except KeyError as ke:
        print(f"KeyError: {ke}. Expected Key not found in the JSON response")
        df = json_normalize(model_responses, record_path=["SOP_Table", "Procedure"])

    except Exception as e:
        print("An unexpected error has occured: {e}")

    # Now to generate images and update the dataframe
    df = generate_images_and_update_df(df, client)
    df.drop(columns=["image_prompt"], inplace=True)

    # Convert dataframe into html
    df_html = df.to_html(
        escape=False, formatters=dict(Example=path_to_image_html), index=False
    )

    # Next we want to convert the JSON response for the summary portion into a flattened pandas dataframe
    try:
        summary = json_normalize(model_responses)
        summary.drop(columns="SOP_Table.Procedure_Steps", inplace=True)

    except KeyError as ke:
        print(f"KeyError: {ke}. Expected Key not found in the JSON response")
        summary = json_normalize(model_responses)
        summary.drop(columns="SOP_Table.Procedure", inplace=True)

    except Exception as e:
        print("An unexpected error has occured - Key not found in summary: {e}")

    # Rename summary columns and convert df to html
    summary.columns = [re.sub("^(.*\.)", "", col) for col in summary.columns]
    summary_html = summary.to_html(index=False)

    # Now to merge both summary html and instruction html in one html page - insert gap between both tables

    # Merge HTML content with a gap between tables
    merged_html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .table-container {{
                margin-bottom: 50px;  /* Adjust the gap between tables */
            }}

            table {{
                border-collapse: collapse;
                width: 50%;
                margin: 20px;
            }}
            th, td {{
                border: 1px solid black;
                padding: 20px;
                text-align: left;
            }}
            h2 {{
                color: blue;
            }}

            body {{ background-color: #e0e0e0; }}
        </style>
    </head>
    <body>
        <h2>Responsibilities and Governance</h2>
            {summary_html}
        <h2>Instructions and Guidelines</h2>
            {df_html}
        </div>
    </body>
    </html>
    """

    # Save the merged HTML content into a new file
    with open(f"{NamingCovention()}.html", "w") as merged_file:
        merged_file.write(merged_html_content)


if __name__ == "__main__":
    main()
