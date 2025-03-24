# Factory Project

## 專案簡介與背景

本專案旨在展示如何在 Django 框架下應用物流運輸與最佳化演算法。透過這個專案，你可以看到如何將使用者認證、資料展示與複雜演算法相結合，模擬實際物流運輸中的路徑規劃與成本比較，進而提升運送效率。此專案同時也展現了如何運用 Django 強大的 ORM 以及模板系統來建立一個結構清晰、易於維護的應用程式。

## 主要功能

* **使用者認證與註冊：** 利用 Django 內建的認證系統，提供註冊、登入與登出的功能，保護應用的敏感頁面。
* **Dashboard 顯示碼頭運作狀況：** 提供各個碼頭的當前載重與歷史運送數據，讓使用者能夠一目瞭然各碼頭的運作情形。
* **成本比較與最佳化路徑計算：** 透過對比原始運送路徑與最佳化演算法計算後的路徑，展示物流運輸成本的變化，並以圖表形式呈現。
* **動態展示機器人運送軌跡：** 以動畫形式展示機器人運送過程中的移動軌跡，直觀呈現物流運作過程。

## 技術棧

* **後端框架：** Django
* **資料庫：** SQLite（開發階段使用，可根據需求調整）
* **前端：** 使用 Django 模板語言搭配基本的 HTML/CSS/JavaScript
* **其他套件：**
   * python-decouple 或 django-environ（用於管理敏感資訊與環境變數）

## 安裝與執行步驟

1. **建立虛擬環境：**
   ```bash
   python -m venv env
   ```

2. **啟動虛擬環境：**
   * Windows:
   ```bash
   env\Scripts\activate
   ```
   * macOS/Linux:
   ```bash
   source env/bin/activate
   ```

3. **安裝依賴：** 確保 `requirements.txt` 文件中已列出所有依賴，然後執行：
   ```bash
   pip install -r requirements.txt
   ```

4. **設定環境變數：** 在專案根目錄下建立一個 `.env` 文件，並加入：
   ```ini
   SECRET_KEY=你的秘密金鑰
   DEBUG=True
   ```
   注意：將 `.env` 文件加入 `.gitignore` 以防止敏感資訊上傳到 GitHub。

5. **執行資料庫遷移：**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **啟動開發伺服器：**
   ```bash
   python manage.py runserver
   ```

7. **訪問應用程式：** 打開瀏覽器並前往 http://127.0.0.1:8000 檢視專案。

## 專案結構

* **factory_project/**
   * `settings.py`：專案設定檔，包含資料庫設定、應用程式安裝、環境變數讀取等。
   * `urls.py`：全域 URL 路由配置。
   * `manage.py`：Django 命令列工具。
* **logistics/**
   * `models.py`：定義碼頭、機器人、運送記錄及倉庫等資料模型。
   * `views.py`：各頁面的視圖函式，負責處理請求與回傳資料。
   * `optimization.py`：包含物流最佳化演算法相關函式。
   * 其他模板與靜態檔案：用於前端頁面展示。

## 配置設定

專案中敏感資訊（例如 SECRET_KEY）不再硬編碼於程式碼中，而是使用環境變數來進行管理。建議使用以下方法之一：

* **python-decouple：** 在 `settings.py` 中使用：
  ```python
  from decouple import config
  SECRET_KEY = config('SECRET_KEY')
  ```

* **django-environ：** 在 `settings.py` 中使用：
  ```python
  import environ
  env = environ.Env(DEBUG=(bool, False))
  environ.Env.read_env()
  SECRET_KEY = env('SECRET_KEY')
  ```

請確保 `.env` 文件不會上傳至 GitHub，並在 `.gitignore` 中加入：
```
.env
```

## 貢獻指南

若你有興趣為此專案做出貢獻，請參考以下步驟：

1. Fork 此儲存庫。
2. 建立你的 feature branch (`git checkout -b feature/你的功能描述`)。
3. 提交你的修改 (`git commit -am '新增功能或修正錯誤'`)。
4. Push 到你的 branch (`git push origin feature/你的功能描述`)。
5. 提交一個 Pull Request。

## 授權條款

本專案採用 MIT License 授權，詳情請參閱 LICENSE 文件。
