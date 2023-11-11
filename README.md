# NTU-Cool-to-Google-Calender

將 NTU Cool 的日曆同步更新至個人 Google 日曆

## 使用方法
### 1.
在終端機中輸入
```bash
git clone https://github.com/NelloHo/NTU-Cool-to-Google-Calender
```

### 2.
在終端機中輸入
```bash
pip install -r requirements.txt
```

### 3.
將`defs.py`中`USERNAME`和`PASSWORD`的值改成你的帳號和密碼(記得保留"")

### 4.
至[google 官網](https://developers.google.com/calendar/api/quickstart/python?hl=zh-tw)分別[啟用 API](https://developers.google.com/calendar/api/quickstart/python?hl=zh-tw#enable_the_api)、[設定 OAuth](https://developers.google.com/calendar/api/quickstart/python?hl=zh-tw#configure_the_oauth_consent_screen)與[授權電腦版應用程式憑證](https://developers.google.com/calendar/api/quickstart/python?hl=zh-tw#authorize_credentials_for_a_desktop_application)


### 5. 
或在終端機中輸入
```bash
python main.py
```
第一次使用會跳出 Google 的存取授權，照著點就好。

