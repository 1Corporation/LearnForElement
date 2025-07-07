import csv
import json


def main():

    result = []

    with open("codefuture_answers.csv", "r") as codefuture_answers:
        reader = csv.reader(codefuture_answers, delimiter='|')
        for row in reader:
            print(row)
            question = row[0]
            answer = row[1]

            result.append({"question": question, "answer": answer})


    with open("result_codefuture_asnwers.json", "w+") as codefuture_json:
        formatted_json = json.dumps(result, indent=4, ensure_ascii=False)
        codefuture_json.write(formatted_json)


if __name__ == '__main__':
    main()
