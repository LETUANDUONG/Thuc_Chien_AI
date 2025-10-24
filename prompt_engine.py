import json
import os
import yaml
import re
import unicodedata
from openai import OpenAI
# ===================================================
# ⚙️ CẤU HÌNH GEMINI + LiteLLM LOCAL
# ===================================================
GEMINI_API_KEY = "sk-1IlnKHUqwXiz5463gmU_nA"
API_BASE = "https://api.thucchien.ai/v1"
MODEL = "gemini-2.5-pro"

client = OpenAI(
    api_key = GEMINI_API_KEY,
    base_url= API_BASE
)
# ===================================================
# 🧩 HÀM HỖ TRỢ
# ===================================================
def slugify(value):
    """
    Converts to lowercase, removes non-word characters, and converts spaces to underscores.
    Also removes diacritics (accents).
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('utf-8')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '_', value) # Replace spaces and hyphens with single underscore
    return value

def call_llm(prompt: str) -> str:
    """Gọi Gemini qua LiteLLM và trả về nội dung text."""
    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return res.choices[0].message.content
    except Exception as e:
        print("❌ Lỗi khi gọi Gemini:", e)
        return ""

def safe_json_parse(text: str):
    """Cố gắng trích JSON hợp lệ từ phản hồi của model."""
    try:
        json_text = re.search(r"\{.*\}|\[.*\]", text, re.DOTALL).group()
        return json.loads(json_text)
    except Exception:
        print("⚠️ Không parse được JSON, dùng raw text thay thế.")
        return text

# ===================================================
# 🧠 ĐỌC DỮ LIỆU ĐỀ BÀI + TEMPLATE
# ===================================================
with open("C:/Users/Admin/Desktop/ai_tt/sample_project.jsonl", "r", encoding="utf-8") as f:
    project = json.load(f)

with open("prompt_instruction.yaml", "r", encoding="utf-8") as f:
    base_template = yaml.safe_load(f)

# ===================================================
# 📋 B1. XÁC ĐỊNH DANH SÁCH CÁC VAI TRÒ
# ===================================================
roles_prompt = f"""
Phân tích dự án sau và liệt kê các vai trò (agents) cần có để hoàn thành sản phẩm.
Mỗi vai trò gồm: tên, id, mô tả ngắn gọn.
Chỉ trả về JSON hợp lệ.

Dự án:
{json.dumps(project, ensure_ascii=False, indent=2)}
"""

roles_text = call_llm(roles_prompt)
roles_data = safe_json_parse(roles_text)

# Nếu model trả về list vai trò → chuẩn hóa danh sách tên
if isinstance(roles_data, list):
    role_names = [r.get("role", r.get("name", "")) for r in roles_data]
else:
    role_names = [r.strip() for r in str(roles_data).splitlines() if r.strip()]

print(f"✅ Đã xác định {len(role_names)} vai trò:")
for r in role_names:
    print(f"   - {r}")

# ===================================================
# 🧱 B2. TẠO PROMPT CHO TỪNG AGENT
# ===================================================
os.makedirs("agents", exist_ok=True)

# Chuyển YAML template sang text một lần (tránh gửi lặp)
template_text = yaml.dump(base_template, allow_unicode=True, sort_keys=False)

for role in role_names:
    role_id = slugify(role)
    prompt = f"""
Tạo prompt YAML hoàn chỉnh cho vai trò: "{role}"
Dựa trên template chuẩn sau:

{template_text}

Thông tin dự án:
- Tên dự án: {project['project_name']}
- Loại sản phẩm: {project['product_type']}
- Chủ đề: {project['theme']}
- Yêu cầu chính: {', '.join(project['requirements'])}
- Phong cách: {project['style']}
- Đối tượng: {project['target_audience']}

Yêu cầu:
- Viết bằng tiếng Việt.
- Đảm bảo đúng cấu trúc YAML, có đủ các trường.
- Mô tả chi tiết nhưng ngắn gọn, dùng được trực tiếp.
"""
    content = call_llm(prompt)
    filename = f"agents/{role_id}.yaml"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🧩 Đã sinh thành công: {filename}")

print("\n🎉 Hoàn tất sinh prompt cho tất cả vai trò.")
