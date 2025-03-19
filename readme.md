# How to setup in local?

<ul>
    <li>Create a virtaul environment with python >= 3.11</li>
    <li>Create a .env file with the API key for weatherstack(use "WEATHER_API_KEY" as key name)</li>
    <li>Install the requirements with <code>pip install -r requirements.txt</code></li>
    <li>Execute <code>bash setup.sh</code> to setup the local LLM environment. sudo access is neede for the setup.</li>
    <li>To access it locally through frontend run the <file>app_local.ipynb</file></li>
    <li>To access the app through API run the <code>python app.py</code></li>
</ul>



## Note
<ul>
    <li>I have used here Llama3.1:8B model(Quantized version of Ollama).</li>
    <li>As, the model is a lightweight model, I have noticed that hallucinations is a problem here. The model performance is good but for better performanbce some bigger models can be used.</li>
    <li>Database is also hosted locally so scalibility is also a problem here.</li>
</ul>


## Example
<p>I am attaching here some demo videos of the app. </p>
<ul>
    <li>Video 1: <a href="https://drive.google.com/file/d/1xj2WB0EvbfGfANdsdTeXrvW2wWK7nLUY/view?usp=sharing" target="_blank">Link</a></li>
    <li>Video 2: <a href="https://drive.google.com/file/d/1qz5kb_JsvwnTFFro_pEQ8cSjL98k2VKu/view?usp=drive_link" target="_blank">Link</a></li>
</ul>


## Deployment Cost
<p>For better peformance we need a GPU machine with minimal 8GB of GPU memory which will cost around 0.8-1$ per hour.</p>
<p>The code can also be executed on CPU machine which will cost 0.5-0.8$ per hour.</p>
<p>The main advantage of local LLM is we don't need to pay any LLM cost to third party vendor and it can also run on shared resources as well as the deployment can go down when there is no traffic.</p>