import ollama


stream = ollama.generate(
    model="llama3",
    prompt="Задай 10 вопросов-ответов к этому участку документации по языку программирования:  ACos: Доступность: КлиентИСервер  Сигнатура - ACos(Число:Число):Число Возвращает арккосинус значения Число. Разговаривай на Русском",
    stream=True
)


for chunk in stream:
    print(chunk["response"], end="", flush=True)
