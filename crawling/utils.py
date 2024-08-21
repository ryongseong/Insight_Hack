import json

def get_source(file_path):
    try:
        print("file_path : ", file_path)

        data = None
        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print("error : ", e)


def output_json_data(file_name, data):
    try:
        # main이 위치한 경로를 기준으로 함
        file_path = f"./sources/outputs/{file_name}.json"
        print("file_path : ", file_path)

        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent="\t")

        print("Created json file.")
        return True
    except Exception as e:
        print("error : ", e)
        return False