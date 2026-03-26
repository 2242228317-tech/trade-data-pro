"""
AI 视频生成自动化脚本
支持：Replicate API / SiliconFlow API
"""

import os
import sys

# 加载 .env 文件
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

# 自动选择 API 提供商
if os.environ.get("SILICONFLOW_API_KEY") and os.environ.get("SILICONFLOW_API_KEY") != "sk-把你的key粘贴到这里":
    PROVIDER = "siliconflow"
    print("[信息] 使用 SiliconFlow API")
    from siliconflow_video import generate_video
elif os.environ.get("REPLICATE_API_TOKEN"):
    PROVIDER = "replicate"
    print("[信息] 使用 Replicate API")
    # Replicate 相关导入在下面
else:
    print("[错误] 未找到 API Key")
    print("请在 .env 文件中设置 SILICONFLOW_API_KEY 或 REPLICATE_API_TOKEN")
    sys.exit(1)

# 原有的 Replicate 代码（当使用 Replicate 时）
if PROVIDER == "replicate":
    import replicate
    import requests
    from datetime import datetime

    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    def generate_image(prompt, width=1024, height=1024):
        """使用 SDXL 生成图像"""
        print(f"[图像生成] {prompt[:50]}...")
        
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            }
        )
        
        image_url = output[0] if isinstance(output, list) else output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"{OUTPUT_DIR}/image_{timestamp}.png"
        
        response = requests.get(image_url)
        with open(image_path, "wb") as f:
            f.write(response.content)
        
        print(f"[完成] 图像保存至: {image_path}")
        return image_path

# 统一的视频生成接口
if PROVIDER == "siliconflow":
    # 已导入 generate_video
    pass

if __name__ == "__main__":
    print("="*50)
    print("AI 视频生成")
    print("="*50)
    print()
    
    if PROVIDER == "siliconflow":
        # SiliconFlow 测试
        test_prompt = "一只可爱的熊猫在竹林里吃竹子，阳光明媚，高清画质"
        result = generate_video(test_prompt, seconds=5)
        if result:
            print(f"\n✅ 成功: {result}")
        else:
            print(f"\n❌ 失败")
    else:
        print("Replicate 模式暂不支持直接运行")
        print("请配置 SiliconFlow API Key")

def generate_image(prompt, width=1024, height=1024):
    """使用 SDXL 生成图像"""
    print(f"[图像生成] {prompt[:50]}...")
    
    output = replicate.run(
        "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
        input={
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "num_inference_steps": 50
        }
    )
    
    # 下载图像
    image_url = output[0] if isinstance(output, list) else output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{OUTPUT_DIR}/image_{timestamp}.png"
    
    response = requests.get(image_url)
    with open(image_path, "wb") as f:
        f.write(response.content)
    
    print(f"[完成] 图像保存至: {image_path}")
    return image_path

def generate_video(prompt, seconds=5, fps=24):
    """使用 Wan 2.1 生成视频"""
    print(f"[视频生成] {prompt[:50]}...")
    print(f"[参数] 时长: {seconds}秒, FPS: {fps}")
    
    num_frames = seconds * fps
    
    output = replicate.run(
        "wavespeedai/wan-2.1-t2v-720p",
        input={
            "prompt": prompt,
            "num_frames": num_frames,
            "fps": fps,
            "width": 720,
            "height": 480,
            "guidance_scale": 5.0
        }
    )
    
    # 下载视频
    video_url = output if isinstance(output, str) else output[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = f"{OUTPUT_DIR}/video_{timestamp}.mp4"
    
    print(f"[下载中] 视频较大，请耐心等待...")
    response = requests.get(video_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(video_path, "wb") as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r[下载进度] {percent:.1f}%", end="", flush=True)
    
    print(f"\n[完成] 视频保存至: {video_path}")
    return video_path

def text_to_speech(text, voice_id="default"):
    """语音合成（待接入 GPT-SoVITS 或 ElevenLabs）"""
    print(f"[语音合成] {text[:50]}...")
    # TODO: 接入语音合成 API
    pass

def create_full_video(script_dict):
    """
    完整视频生成流程
    
    script_dict 格式:
    {
        "title": "视频标题",
        "scenes": [
            {"desc": "场景描述", "duration": 5},
            ...
        ],
        "voiceover": "旁白文本"
    }
    """
    print("="*50)
    print(f"开始生成视频: {script_dict['title']}")
    print("="*50)
    
    generated_files = []
    
    # 1. 生成每个场景的素材
    for i, scene in enumerate(script_dict['scenes']):
        print(f"\n[场景 {i+1}/{len(script_dict['scenes'])}]")
        
        # 生成图像/视频
        if scene.get('duration', 5) <= 3:
            # 短场景用图片
            img = generate_image(scene['desc'])
            generated_files.append({"type": "image", "path": img})
        else:
            # 长场景用视频
            vid = generate_video(scene['desc'], seconds=scene.get('duration', 5))
            generated_files.append({"type": "video", "path": vid})
    
    print("\n" + "="*50)
    print("生成完成！")
    print(f"输出目录: {os.path.abspath(OUTPUT_DIR)}")
    print("="*50)
    
    return generated_files

if __name__ == "__main__":
    # 测试示例
    test_script = {
        "title": "赛博朋克城市",
        "scenes": [
            {"desc": "A futuristic cyberpunk city at night, neon lights, flying cars, rain, blade runner style", "duration": 5}
        ]
    }
    
    print("AI 视频生成测试")
    print("请确保已设置 REPLICATE_API_TOKEN 环境变量")
    print()
    
    try:
        result = create_full_video(test_script)
        print(f"\n成功生成 {len(result)} 个素材")
    except Exception as e:
        print(f"\n[错误] {e}")
        print("提示: 请检查 REPLICATE_API_TOKEN 是否设置正确")
