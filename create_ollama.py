import ollama
import json


#stream = ollama.chat(
#	model="mistral",
#	messages=[{"role": "system", "content": "Отвечай исключительно на русском языке. Я буду отправлять тебе участки документации. Сгенерируй 5 пар вопросов-ответов по данному участку докуменации, по языку программирования. Нельзя использовать информацию, которой нет участке документации. Ответ отправь в формате json с ключами question и answer"}, {"role": "user", "content": "ACos(Число:Число):Число - Возвращает арккосинус значения Число. "}],
#	options={"temperature": 0.3}
#)



def main():

    result = []

    with open("test.json", "r", encoding="utf-8") as file:

        docs = json.load(file)

        for method in docs:

            response = ollama.generate(
            	model="mistral",
            	prompt=f"""SYSTEM: 
            	Ты — помощник-разработчика. Твоя задача — СТРОГО использовать только информацию из описания метода и НИЧЕГО больше. Если информация о каком‑то аспекте не указана в описании, не придумывай допущений и не расширяй тему.
            	
            	USER:
            	Название метода: {method}
            	Описание: Описание: {docs[method]}. 
            	
            	INSTRUCTION:
            	Сгенерируй ровно 5 пар «Вопрос – Ответ» на русском языке по данному методу. 
            	- Вопросы и ответы должны опираться только на то, что есть в описании.
            	- Не упоминай языки программирования или библиотеки, если они явно не указаны.
            	- Давай разнообразные по типу вопросы: про назначение, входные параметры, возможные ошибки, примеры использования и т. п.
            	
            	Формат вывода

            	  [
                    {{
                      \"question\": \"Как сделать это?\",
                      \"answer\": \"вот так\",
                    }},
                    {{
                      \"question\": \"Почему это?\",
                      \"answer\": \"Потому что.\"
                    }}
                ]
                """,
            	options={
            	    "temperature": 0.3,
            	    "top_p": 0.8,
            	    "repeat_penalty": 1.15,
            	    "num_predict": 768
            	}
            )

            print(response["response"])
            result += json.loads(response["response"])

            print("result - ", result)

    with open("qa,json", "w+") as qa:
        result_json = json.dumps(result, indent=4, ensure_ascii=False)
        qa.write(result_json)
    
if __name__ == "__main__":
    main()
