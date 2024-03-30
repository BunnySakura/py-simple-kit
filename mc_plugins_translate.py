from pathlib import Path
import json
import requests


def translator(word: str) -> str:
    response_json = requests.get(
        url="http://fanyi.youdao.com/translate?&doctype=json&type=EN2ZH_CN&i=" + word
    )
    translation = response_json.json()["translateResult"][0][0]["tgt"]
    return translation


def json_loads(file: Path):
    # 读取并翻译
    with file.open('r') as f:
        json_data = json.loads(f.read())
        for i in json_data:
            print(i + "\t:", end='')
            if isinstance(json_data[i], str):  # 判断是否为字符串
                json_data[i] = translator(json_data[i])
                print(json_data[i])
            else:
                print()
                pass

    # 保存
    json_data = json.dumps(json_data, ensure_ascii=False)
    with file.open('w') as f:
        f.write(json_data)


if __name__ == "__main__":
    directory = Path("./")
    for file in directory.glob("*.json"):
        json_loads(file)
