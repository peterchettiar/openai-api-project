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
