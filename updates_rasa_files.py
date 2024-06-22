import pandas as pd
import yaml

# Chemins vers les fichiers existants
nlu_file_path = 'data/nlu.yml'
stories_file_path = 'data/stories.yml'
domain_file_path = 'domain.yml'
csv_file_path = './data/data_train_extend.csv'

# Charger les fichiers existants
with open(nlu_file_path, 'r', encoding='utf-8') as file:
    nlu_data = yaml.safe_load(file)

with open(stories_file_path, 'r', encoding='utf-8') as file:
    stories_data = yaml.safe_load(file)

with open(domain_file_path, 'r', encoding='utf-8') as file:
    domain_data = yaml.safe_load(file)

# Charger les nouvelles données
data = pd.read_csv(csv_file_path)

# Ajouter les nouvelles intentions et exemples
for _, row in data.iterrows():
    question = row['questions'].strip()
    intent = "handle_" + question.replace(" ", "_").replace("'", "").lower()
    example = f"- {question}"

    # Vérifier si l'intention existe déjà
    existing_intent = next((item for item in nlu_data['nlu'] if item['intent'] == intent), None)
    if existing_intent:
        # Ajouter l'exemple à l'intention existante
        existing_intent['examples'] += f"\n{example}"
    else:
        # Ajouter une nouvelle intention
        nlu_data['nlu'].append({
            'intent': intent,
            'examples': example
        })

# Ajouter aux Histoires
for _, row in data.iterrows():
    question = row['questions'].strip()
    response = row['reponses'].strip()
    intent = "handle_" + question.replace(" ", "_").replace("'", "").lower()
    action = "utter_" + intent

    stories_data['stories'].append({
        'story': f"Story for {intent}",
        'steps': [
            {'intent': intent},
            {'action': action}
        ]
    })

# Ajouter aux Réponses et Intentions dans domain.yml
for _, row in data.iterrows():
    question = row['questions'].strip()
    response = row['reponses'].strip()
    intent = "handle_" + question.replace(" ", "_").replace("'", "").lower()
    action = "utter_" + intent

    # Ajouter l'intention
    if intent not in domain_data['intents']:
        domain_data['intents'].append(intent)

    # Ajouter la réponse
    domain_data['responses'][action] = [{'text': response}]

# Sauvegarder les fichiers mis à jour
with open(nlu_file_path, 'w', encoding='utf-8') as file:
    yaml.dump(nlu_data, file, allow_unicode=True)

with open(stories_file_path, 'w', encoding='utf-8') as file:
    yaml.dump(stories_data, file, allow_unicode=True)

with open(domain_file_path, 'w', encoding='utf-8') as file:
    yaml.dump(domain_data, file, allow_unicode=True)
