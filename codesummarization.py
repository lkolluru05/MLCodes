import vertexai
from vertexai.language_models import CodeGenerationModel
from bs4 import BeautifulSoup

#text=""
file_path = "sample1.html"
with open(file_path, 'r') as file:
    html = file.read()

    #soup = BeautifulSoup(html, 'html.parser')

    # Extract text content
    #text = soup.get_text(separator=' ', strip=True)
    #text = "Please summarize the code : "+ text 

    # TODO(developer): update project_id, location & temperature
vertexai.init(project="cmetestproj", location="us-central1")
parameters = {
        "temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        #"top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        #"top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
}

model = CodeGenerationModel.from_pretrained("code-bison@002")
response = model.predict(html,**parameters)
print(f"Response from Model: {response.text}")