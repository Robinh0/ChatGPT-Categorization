import pandas as pd
import openai
import time

categorien_v29 = """
[Looptijd contracten,
Gezinssamenstelling,
Veranderingen in energiekosten
Maatregelen voor energiebesparing
Overstappen naar andere energieleveranc,
Invloed van COVID-19,
Veranderingen in energiegebruik,
Onzekerheden in verbruik,
Invloed van belastingen en accijnzen,
Overige redenen,
Onbekend]
"""

categorien_v6 = """
[Isolatie,
Zonnepanelen,
Dubbel glas,
Elektriciteitsbesparing,
Van het gas af gaan,
Verwarming,
LED verlichting,
Energiebesparing,
Kunststof ramen en deuren,
Overige redenen,
Onbekend]
"""

def long_prompt(data, categorien):
    return f"""
    Jij bent een consumer & marktonderzoek specialist. 
    Je onderzoekt enquetedata over energieverbruik van het huis, en over de motivatie om te verduurzamen in huis.
    
    lijst met categorien =
    {categorien}
    
    data = {data}
    
    Vragen:
    1. Wat is het sentiment van <data> over het algemeen? positief/neutraal/negatief/n.v.t. --> <algemeen sentiment>
    2. Welke categorie van <lijst met categorien> past goed bij <data>? Meerdere opties mogelijk. --> <categorie>
    3. Welk sentiment bevat de context rondom de categorie van <data>? positief/neutraal/negatief/n.v.t. --> <sentiment>
    
    Antwoord op de volgende manier, zonder nummers:
    Antwoord: <algemeen sentiment> ## <categorie>, <sentiment> // <categorie>, <sentiment>
    """


def short_prompt(data, categorien):
    return f"""
    Jij bent een consumer & marktonderzoek specialist. 
    Je onderzoekt enquetedata over energieverbruik van het huis, en over de motivatie om te verduurzamen in huis.

    lijst met categorien =
    {categorien}
    
    data = {data}

    Vragen:
    1. Wat is het sentiment van <data> over het algemeen? positief/neutraal/negatief/n.v.t. --> <algemeen sentiment>
    2. Welke categorie van <lijst met categorien> past het beste bij <data>? --> <categorie>

    Antwoord op de volgende manier, zonder nummers:
    Antwoord: <algemeen sentiment> ## <categorie>
    """


def openAI_request(data):
    openai.api_key = "enter-api-key-here"
    result = None
    data_words = data.split()
    categorien = categorien_v29

    while result is None:
        if len(data_words) >= 5:
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=long_prompt(data, categorien),
                    temperature=0.3,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.6,
                    stop=[" Human:", " AI:"]
                )

                result = response['choices'][0]['text']
                return result
            except:
                time.sleep(5)
                print("Sleeping, zZz.")
        else:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=short_prompt(data, categorien),
                temperature=0.3,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )

            result = response['choices'][0]['text']
            return result


file = "V29_sample_data"
df = pd.read_excel(f"{file}.xlsx")
counter = 0

for index, row in df.iterrows():
    text = row["data"]
    if text != None:
        # print(f"Question on index {index}")
        # print(f"Text to analyze:\n{text}")

        data = openAI_request(text)
        print(data)

        df.at[index, "Answer"] = f"{data}".strip()

        df.to_excel(f"{file}_results.xlsx", index=False)

        counter += 1

        if counter == 50:
            break

