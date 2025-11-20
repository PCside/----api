import os
import random
import time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルのマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# 画像保存フォルダの定義
IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_seal_image(filename):
    """
    【画像生成ロジック】
    ここではAIの代わりに、Pythonの機能でランダムな色の
    「あざらしっぽい（概念）」画像を生成して保存します。
    ※ここにDALL-EなどのAPIを組み込めば本物のAI生成になります。
    """
    width, height = 512, 512
    
    # ランダムな背景色
    bg_color = (random.randint(200, 255), random.randint(230, 255), 255) # 水色系
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # あざらし（のような白い楕円）を描画
    draw.ellipse((100, 150, 412, 362), fill=(240, 240, 240), outline=(200, 200, 200))
    
    # 目
    draw.ellipse((180, 220, 200, 240), fill=(0, 0, 0))
    draw.ellipse((312, 220, 332, 240), fill=(0, 0, 0))
    
    # 鼻と口
    draw.ellipse((246, 260, 266, 280), fill=(0, 0, 0))
    
    # テキスト追加（IDなど）
    # フォントがない環境でのエラーを防ぐためデフォルトを使用
    draw.text((20, 20), f"Seal ID: {random.randint(1000, 9999)}", fill=(0, 100, 100))

    # ファイルに保存
    file_path = os.path.join(IMAGE_DIR, filename)
    img.save(file_path)
    return file_path

@app.get("/api/seal")
def get_and_generate_seal(request: Request):
    """
    画像を生成(GET)してURLを返す
    """
    # ユニークなファイル名を生成 (例: seal_1709283.png)
    filename = f"seal_{int(time.time())}_{random.randint(0,100)}.png"
    
    try:
        # 画像生成関数を呼び出し
        generate_seal_image(filename)
        
        # URLを作成
        base_url = str(request.base_url).rstrip("/")
        image_url = f"{base_url}/static/images/{filename}"

        return {
            "message": image_url,
            "status": "success",
            "generated": True
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)