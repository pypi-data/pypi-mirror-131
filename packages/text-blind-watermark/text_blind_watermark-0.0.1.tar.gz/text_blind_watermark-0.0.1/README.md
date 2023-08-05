# text_blind_watermark
Put blind watermark into a text.

Can be used in 
- [x] Wechat
- [x] dingding
- [x] ...

## How to Use

### Alice Put her text watermark into a text:

```python
from text_blind_watermark import embed, extract

wm = "绝密：两点老地方见！"
password = '20190808'
sentence = "这句话中有盲水印，你能提取出来吗？" * 16

sentence_embed = embed(sentence, wm, password)
print("打上盲水印之后")
print(sentence_embed)
```

Then, you can paste this text to where you need.


*It uses AES to encrypt*

### Bob Extract the invisible watermark

```python
wm_extract = extract(sentence_embed, password)
print("解出的盲水印")
print(wm_extract)
```

