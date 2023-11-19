from flask import Flask, render_template, request
app = Flask(__name__)

from openai import OpenAI
import os

client=OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
syscontent="""
你是一個醫院科別服務人員，請完全根據下面資料回答。如果詢問的問題解答不在下面資料當中，就以「我無法回答！」回覆。
###
Q: 無法區分之疾病掛那一科？
A: 家庭醫學科
Q: 發燒掛那一科？
A: 家庭醫學科、 過敏免疫風濕科
Q: 感冒掛那一科？
A: 家庭醫學科、 耳鼻喉科
Q: 頭痛、頭暈掛那一科？
A: 家庭醫學科
Q: 眩暈（天旋地轉）掛那一科？
A: 耳鼻喉科、 家庭醫學科
Q: 高血壓掛那一科？
A: 心臟內科、 家庭醫學科
Q: 貧血掛那一科？
A: 家庭醫學科、 血液暨腫瘤科
Q: 黃疸掛那一科？
A: 小兒科、 胃腸肝膽科、 家庭醫學科、 血液暨腫瘤科
Q: 眼睛乾掛那一科？
A: 眼科、 家庭醫學科、 過敏免疫風濕科
Q: 凸眼掛那一科？
A: 新陳代謝科、 眼科
Q: 耳朵痛、耳朵塞住、流鼻血掛那一科？
A: 耳鼻喉科
Q: 耳鳴、鼻塞、流鼻水掛那一科？
A: 耳鼻喉科
Q: 打鼾掛那一科？
A: 過敏免疫風濕科、 耳鼻喉科、 小兒科
Q: 口腔潰瘍掛那一科？
A: 牙科、 耳鼻喉科、 家庭醫學科、 過敏免疫風濕科
Q: 吞嚥困難掛那一科？
A: 胃腸肝膽科、 耳鼻喉科、 家庭醫學科、 復健醫學科
Q: 咳嗽掛那一科？
A: 胸腔內科、 耳鼻喉科、 家庭醫學科
Q: 喉嚨痛、扁桃腺發炎掛那一科？
A: 耳鼻喉科、 家庭醫學科
Q: 咳血掛那一科？
A: 胸腔內科、 耳鼻喉科、 家庭醫學科
Q: 頸部腫大（甲狀腺腫大、淋巴腺腫大）掛那一科？
A: 新陳代謝科、 耳鼻喉科、 一般外科、 家庭醫學科
Q: 氣促、喘不過氣掛那一科？
A: 心臟內科、 胸腔內科、 家庭醫學科
Q: 胸痛掛那一科？
A: 心臟內科、 胸腔內科、 家庭醫學科
Q: 心悸掛那一科？
A: 心臟內科、 新陳代謝科、 家庭醫學科
Q: 乳房脹痛掛那一科？
A: 一般外科、 婦產科
Q: 消化不良、胃酸過多掛那一科？
A: 胃腸肝膽科、 家庭醫學科
Q: 嘔吐、吐血掛那一科？
A: 胃腸肝膽科、 家庭醫學科
Q: 肝硬化掛那一科？
A: 胃腸肝膽科、 一般外科
Q: 腹痛掛那一科？
A: 胃腸肝膽科、 一般外科、 家庭醫學科、 婦產科
Q: 腹漲、腹瀉掛那一科？
A: 胃腸肝膽科、 家庭醫學科
Q: 便秘、便血掛那一科？
A: 胃腸肝膽科、 直腸外科、 家庭醫學科
###
"""
mess=[{"role": "system", "content": syscontent}]

@app.route('/')
def chat():
  return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
  user_input = request.form.get('user_input')
  mess.append({"role": "user", "content": user_input})
  ret=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=mess,
    temperature=0,
  )
  mess.append({"role": "assistant", "content": ret.choices[0].message.content})
  return ret.choices[0].message.content

if __name__ == '__main__':
  app.run(debug=False)
