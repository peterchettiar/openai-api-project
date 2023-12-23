# openai-api-project
A simple project to generate Standard Operating Procedures (SOP) using openai api

## Motivation
Full disclosure, this is my first time working with the openai api. And I had no intentions of doing so until recently where I had attended multiple interviews with Tiktok/Bytedance, which got me really curious/interested as well as made me realise the importance of AI.

So in my assessment centre stage of the application process, the task given to me was to create a tool that can help generate SOPs using GenAI. I did not have to code anything but rather set-up a framework of how to do so. I would like to belive that I came up with the process with the requisite open-source tools that can help achieve the goal, but it really got me thinking if it was technically feasible.

Hence, my decision on working on this rather simple project. It's not perfect, which will be discussed as we go along, but its a good enough starting point I guess.

## Setting-up of environment

Typically it would be good to start a project by first creating a virtual environment and subsequently installing all the dependencies necessary for the project before proceeding. But I decided to use my base environment instead, but if you decide to proceed with the proper approach please see [how to set-up virtual environment](https://github.com/peterchettiar/personal-projects?tab=readme-ov-file#2-setting-up-a-new-environment).

## Project Framework and description

![openai](https://github.com/peterchettiar/openai-api-project/assets/89821181/e472585b-7cbc-4c25-8765-ed440a3ad111)

### Step 1: Connecting to the OpenAI Api

The first thing you want to do is to create an account if you haven't done so on the OpenAI platform. As it goes with other similar platforms, you get some free credit when you open an account. Alternatively, you can purchase credits depending on your usage (the platform deploys a 'pay as you go' sort of service). 

Once you've done so, you need to go [here](https://platform.openai.com/api-keys) to create your api key. Next, in your IDE (e.g. VSCode) create a `.env` file in your project directory. Make sure that you save the environment variable in this format `OPENAI_API_KEY="Your personal api key info goes here"`.

## Step 2: Ask users for input

So the context given to me was that ideally the goal is to create a tool that can help generate standard SOPs, and as an example I was given a sample SOP for Image Annotation - Instructions from project managers and data modellers to data labellers. 

With that in mind, I had framed a series of questions for users to input, and subsequently their responses were to be used as prompts into the model. Please find the following table:

![table](https://github.com/peterchettiar/openai-api-project/assets/89821181/8a1a8395-3934-4336-aba9-7ca42c80c3d5)

It should be noted that all the prompt variables except for context are conversational messages to chat with the model. Some would argue that all the prompts, including context, could be combined into one paragraph and fed once into the model. But there were a lot of users who mentioned that running a chat converations would lead to more objective expected outputs. Hence this approach.

## Step 3: Setting of variables

I think the only thing worth mentioning in this section is that I had used `gpt-4-1106-preview` as the chat model of choice. Just wanted to have a feel of the difference compared to using the 3.5 version. As for the image generating model, I used the `dall-e-3` model. Figured that most of us are visual learners, so having images as examples for illustrating what the data annotators should be doing for each step of the SOP would be useful, and should be a standardised practice when setting such SOPs.

## Step 4: Running the chat conversation

The following code block forms the crux of usage of the openai api for text conversations. That is pretty much it. The important part to note is that when you are having a multi-step conversation, you need save your response and use it as input in the next iteration so that it provides context or assists your next question. Hence, the role for that message is `assistant`. Also, to create a deterministic state, we set the temperature and seed arguments. This is really where it gets tricky, even after setting the temperature and seed arguments there is still some possibility that the response does change albeit not too far off. In my situation, I've had responses where the name of the column in question could be either procedure or procedure_steps. Hence, the try and except blocks following this in the main script ([final_script](https://github.com/peterchettiar/openai-api-project/blob/main/SOP-generator-script.py))

```
def GetMessageMemory(NewQuestion, PreviousResponse, systemContext):
    if PreviousResponse is not None:
        response = client.chat.completions.create(
            model=model_input.model_id,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": systemContext},
                {"role": "user", "content": NewQuestion},
                {"role": "assistant", "content": PreviousResponse},
            ],
            temperature=0,
            seed=42
            )
    else:
        response = client.chat.completions.create(
            model=model_input.model_id,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": systemContext},
                {"role": "user", "content": NewQuestion}
            ],
            temperature=0,
            seed=42
            )

    return response.choices[0].message.content

```
## Step 5 - 10

The rest of the steps are rather straight forward. You noramlise the responses into a dataframe and add the `image_prompt` column, which is simply the concatenation of the strings in the first three columns in the procedure_steps dataframe. This image prompt would be used as input in the `dall-e-3` to generate the images needed to be used as an illustrative example to data labellers. The openai model gives you a URL to the image, so you need to convert it into a HTML page in order to display the images.

The same JSON Response also provides a sort of summary page, so we repeat the same steps as we did for the procedure dataframe, and then finally combine both the html tables into one htmal page.

That is pretty much it. This is how the final output should look like:

![Screenshot 2023-12-23 at 11 11 56 PM](https://github.com/peterchettiar/openai-api-project/assets/89821181/3f21c3d2-4ed8-4837-ac03-cf1e6d2dd6bd)
